@preconcurrency import AVFoundation
import Foundation
import NaturalLanguage
import Speech

/// About a sentence of what's said in a recording, and when: at most 40 words or 20 seconds.
public struct SpokenLine: Sendable, Equatable {
    public let start: Double
    public let end: Double
    public let text: String

    public init(start: Double, end: Double, text: String) {
        self.start = start
        self.end = end
        self.text = text
    }
}

/// What listening to a recording found (`Speech.heard(in:)`).
public enum Heard: Sendable, Equatable {
    /// Listening is turned off (`IndexOptions.speech`).
    case off
    /// This Mac can't transcribe now (before macOS 26, or no model for the language and no way to download it): a later
    /// process tries again.
    case unavailable
    /// The recording's sound can't be decoded.
    case unreadable
    /// No speech: music, noise, silence, or a language this Mac has no model for.
    case nothing
    /// What's said, in `language` (the transcriber's locale, "es_ES").
    case said([SpokenLine], language: String)

    public var lines: [SpokenLine] {
        if case .said(let lines, _) = self { return lines }
        return []
    }

    /// Notes the outcome in a file's info: `speech` (the language, "none", "unreadable" or "unavailable") and
    /// `speech_version`, which marks the recording as listened to (`IndexStore.unheard`). An unavailable one isn't.
    func note(in info: inout [String: String]) {
        switch self {
        case .off: return
        case .unavailable:
            info["speech"] = "unavailable"
            return
        case .unreadable: info["speech"] = "unreadable"
        case .nothing: info["speech"] = "none"
        case .said(_, let language): info["speech"] = language
        }
        info["speech_version"] = Speech.version
    }

    /// For the indexer's notes and tallies.
    var summary: String {
        switch self {
        case .off: "off"
        case .unavailable: "unavailable"
        case .unreadable: "unreadable"
        case .nothing: "none"
        case .said(let lines, let language): "\(lines.count) spoken lines (\(language))"
        }
    }
}

/// What's said in audio and video, transcribed on this Mac by Apple's SpeechAnalyzer (macOS 26): no network, about
/// 100× faster than real time (2026-10-16: a 3-minute podcast in 1 s), each word with its time and how sure the
/// transcriber is of it. Lines of about a sentence are embedded as text and kept for keyword search, so a search finds
/// the moment something is said ("Por lo que se dice en 1:47").
///
/// The language: a stretch is transcribed first in the Mac's own language, then the words are given to Apple's language
/// recognizer. A transcriber writes English heard as Spanish in English words, and Spanish heard as English in Spanish
/// ones, so this is clear-cut (1.00 on the demo's 6 recordings, both ways) where the transcribers' confidence wasn't
/// (English: 0.88 in English, 0.84 in Spanish).
public enum Speech {
    /// A new version listens to every recording again, on its own: their frames and sound windows are kept
    /// (`Indexer.listen`).
    public static let version = "1"
    /// The longest stretch of a recording transcribed (from its start): ~2½ minutes of work.
    static let limit = 4 * 3600.0

    public static let isAvailable: Bool = {
        if #available(macOS 26, *) { return SpeechTranscriber.isAvailable }
        return false
    }()

    /// What's said in the recording at `url`. Never throws: problems are outcomes.
    public static func heard(in url: URL) -> Heard {
        do {
            return try transcript(of: url)
        } catch Trouble.unreadable(_) {
            return .unreadable
        } catch {
            return .unavailable
        }
    }

    /// `heard(in:)`, with the reason when it can't listen (`biblo listen`).
    public static func transcript(of url: URL) throws -> Heard {
        guard #available(macOS 26, *) else { throw Trouble.unavailable("needs macOS 26") }
        guard SpeechTranscriber.isAvailable else { throw Trouble.unavailable("this Mac has no speech transcriber") }
        return try runBlocking { try await Listener.heard(in: url) }
    }

    enum Trouble: Error, CustomStringConvertible {
        case unreadable(String)
        case unavailable(String)

        var description: String {
            switch self {
            case .unreadable(let why): "can't decode the sound: \(why)"
            case .unavailable(let why): "can't transcribe: \(why)"
            }
        }
    }

    struct Word: Sendable, Equatable {
        let start: Double
        let end: Double
        /// As the transcriber wrote it: with the space before it, and its punctuation.
        let text: String
        let confidence: Double?
    }

    /// The average confidence of the words that have one.
    static func confidence(_ words: some Collection<Word>) -> Double? {
        let known = words.compactMap(\.confidence)
        return known.isEmpty ? nil : known.reduce(0, +) / Double(known.count)
    }

    /// Words into lines of about a sentence. A sentence ends at its full stop (or ? ! …), at a pause over 1.2 s, or at
    /// 40 words or 20 s. A short sentence ("Exactly.") joins the line before it, as does any sentence after a short line,
    /// up to those limits, and never across a pause. A line the transcriber was unsure of (0.35 or less on average:
    /// music, noise, crosstalk) is left out.
    static func lines(_ words: [Word]) -> [SpokenLine] {
        let (maxWords, maxSeconds, pause) = (40, 20.0, 1.2)
        var sentences: [[Word]] = []
        var sentence: [Word] = []
        for word in words {
            if let last = sentence.last, word.start - last.end > pause {
                sentences.append(sentence)
                sentence = []
            }
            sentence.append(word)
            if endsSentence(word.text) || sentence.count >= maxWords || word.end - sentence[0].start >= maxSeconds {
                sentences.append(sentence)
                sentence = []
            }
        }
        if !sentence.isEmpty { sentences.append(sentence) }

        var lines: [[Word]] = []
        for sentence in sentences {
            if let line = lines.last {
                let fits = line.count + sentence.count <= maxWords && sentence.last!.end - line[0].start <= maxSeconds
                let short = (line.count < 12 && line.last!.end - line[0].start < 6) || sentence.count < 6
                if fits, short, sentence[0].start - line.last!.end <= pause {
                    lines[lines.count - 1] += sentence
                    continue
                }
            }
            lines.append(sentence)
        }
        return lines.compactMap { line in
            let text = line.map(\.text).joined().trimmingCharacters(in: .whitespacesAndNewlines)
            guard !text.isEmpty, (confidence(line) ?? 1) > 0.35 else { return nil }
            return SpokenLine(start: line[0].start, end: line.last!.end, text: text)
        }
    }

    private static func endsSentence(_ word: String) -> Bool {
        let closing: Set<Character> = ["\"", "'", "”", "’", "»", ")", "]", "」", "』"]
        var text = Substring(word.trimmingCharacters(in: .whitespacesAndNewlines))
        while let last = text.last, closing.contains(last) { text = text.dropLast() }
        return text.last.map { ".?!…。？！".contains($0) } ?? false
    }
}

@available(macOS 26, *)
enum Listener {
    static func heard(in url: URL) async throws -> Heard {
        let asset = AVURLAsset(url: url)
        let duration: Double
        do {
            guard !(try await asset.loadTracks(withMediaType: .audio)).isEmpty else { return .nothing }
            duration = try await asset.load(.duration).seconds
        } catch {
            throw Speech.Trouble.unreadable("\(error)")
        }
        guard duration.isFinite, duration >= 1 else { return .nothing }

        let candidates = await Languages.candidates()
        guard let probing = await Languages.ready(candidates) else {
            throw Speech.Trouble.unavailable("no speech model for \(candidates.map(\.identifier)) on this Mac")
        }
        // Which language: a stretch in any language says (a short recording: all of it; a long one: 30 s a fifth of the
        // way in, past intros and music, and 30 s more past the middle if that was quiet).
        let whole = duration <= 45
        var probe: [Speech.Word] = []
        for start in whole ? [0] : [min(duration * 0.2, 120), duration * 0.6] {
            probe = try await transcribe(url, locale: probing, from: start, seconds: whole ? nil : 30)
            if probe.count >= 3 { break }
        }
        guard probe.count >= 3 else { return .nothing }
        var locale = probing
        if let spoken = Languages.language(of: probe), spoken != Languages.code(probing),
           let match = await Languages.locale(for: spoken, among: candidates) {
            locale = match
        }
        let words = whole && locale == probing ? probe : try await transcribe(url, locale: locale, seconds: Speech.limit)
        // Speech in the language it's transcribed in scores 0.77–0.95, in another one 0.30–0.66 (2026-10-16).
        guard words.count >= 3, (Speech.confidence(words) ?? 1) >= 0.5 else { return .nothing }
        let lines = Speech.lines(words)
        return lines.isEmpty ? .nothing : .said(lines, language: locale.identifier)
    }

    /// The words said from `start` (seconds), for `seconds` or to the end, with their times in the recording.
    static func transcribe(_ url: URL, locale: Locale, from start: Double = 0, seconds: Double? = nil) async throws
        -> [Speech.Word] {
        let transcriber = SpeechTranscriber(locale: locale, transcriptionOptions: [], reportingOptions: [],
                                            attributeOptions: [.audioTimeRange, .transcriptionConfidence])
        guard let format = await SpeechAnalyzer.bestAvailableAudioFormat(compatibleWith: [transcriber]) else {
            throw Speech.Trouble.unavailable("no audio format for \(locale.identifier)")
        }
        let isFloat = format.commonFormat == .pcmFormatFloat32
        let reader: AVAssetReader, output: AVAssetReaderTrackOutput
        do {
            let asset = AVURLAsset(url: url)
            guard let track = try await asset.loadTracks(withMediaType: .audio).first else { return [] }
            reader = try AVAssetReader(asset: asset)
            if start > 0 || seconds != nil {
                reader.timeRange = CMTimeRange(start: CMTime(seconds: start, preferredTimescale: 1000),
                                               duration: seconds.map { CMTime(seconds: $0, preferredTimescale: 1000) }
                                                   ?? .positiveInfinity)
            }
            output = AVAssetReaderTrackOutput(track: track, outputSettings: [
                AVFormatIDKey: kAudioFormatLinearPCM, AVSampleRateKey: format.sampleRate, AVNumberOfChannelsKey: 1,
                AVLinearPCMBitDepthKey: isFloat ? 32 : 16, AVLinearPCMIsFloatKey: isFloat,
                AVLinearPCMIsBigEndianKey: false, AVLinearPCMIsNonInterleaved: false,
            ])
            reader.add(output)
            guard reader.startReading() else { throw reader.error ?? Speech.Trouble.unreadable("can't start reading") }
        } catch {
            throw Speech.Trouble.unreadable("\(error)")
        }

        let (stream, input) = AsyncStream<AnalyzerInput>.makeStream()
        let analyzer = SpeechAnalyzer(modules: [transcriber])
        do {
            try await analyzer.start(inputSequence: stream)
        } catch {
            reader.cancelReading()
            throw Speech.Trouble.unavailable("\(error)")
        }
        let collect = Task { () -> [Speech.Word] in
            var words: [Speech.Word] = []
            for try await result in transcriber.results {
                for run in result.text.runs {
                    guard let range = run.audioTimeRange else { continue }
                    words.append(Speech.Word(start: start + range.start.seconds, end: start + range.end.seconds,
                                             text: String(result.text[run.range].characters),
                                             confidence: run.transcriptionConfidence))
                }
            }
            return words
        }

        // Decoded a buffer at a time (memory stays small for a 3-hour podcast) and streamed to the analyzer.
        let bytesPerFrame = Int(format.streamDescription.pointee.mBytesPerFrame)
        while let sample = output.copyNextSampleBuffer() {
            guard let block = CMSampleBufferGetDataBuffer(sample) else { continue }
            let length = CMBlockBufferGetDataLength(block)
            let frames = AVAudioFrameCount(length / bytesPerFrame)
            guard frames > 0, let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frames) else { continue }
            buffer.frameLength = frames
            let destination = isFloat ? UnsafeMutableRawPointer(buffer.floatChannelData![0])
                : UnsafeMutableRawPointer(buffer.int16ChannelData![0])
            CMBlockBufferCopyDataBytes(block, atOffset: 0, dataLength: Int(frames) * bytesPerFrame,
                                       destination: destination)
            input.yield(AnalyzerInput(buffer: buffer))
        }
        input.finish()
        if reader.status == .failed {
            await analyzer.cancelAndFinishNow()
            collect.cancel()
            throw Speech.Trouble.unreadable("\(reader.error.map { "\($0)" } ?? "decoding failed")")
        }
        do {
            try await analyzer.finalizeAndFinishThroughEndOfInput()
            return try await collect.value
        } catch {
            throw Speech.Trouble.unavailable("\(error)")
        }
    }
}

/// The languages recordings are transcribed in, and their models (downloaded by the system, shared by every app).
@available(macOS 26, *)
enum Languages {
    /// The languages a recording is most likely in: the Mac's first three, then English.
    static func candidates() async -> [Locale] {
        var out: [Locale] = []
        for id in Array(Locale.preferredLanguages.prefix(3)) + ["en-US"] {
            guard let locale = await SpeechTranscriber.supportedLocale(equivalentTo: Locale(identifier: id)),
                  !out.contains(where: { code($0) == code(locale) }) else { continue }
            out.append(locale)
        }
        return out
    }

    static func code(_ locale: Locale) -> String {
        locale.language.languageCode?.identifier ?? locale.identifier
    }

    /// The language of what a transcriber wrote ("es"), if the recognizer is sure enough.
    static func language(of words: [Speech.Word]) -> String? {
        let recognizer = NLLanguageRecognizer()
        recognizer.processString(words.map(\.text).joined())
        guard let (language, probability) = recognizer.languageHypotheses(withMaximum: 1).first, probability >= 0.6
        else { return nil }
        return String(language.rawValue.prefix { $0 != "-" })
    }

    /// A language to listen in first: the first candidate that's installed (downloaded now if none is), else any
    /// installed language.
    static func ready(_ candidates: [Locale]) async -> Locale? {
        let installed = await SpeechTranscriber.installedLocales
        if let found = candidates.first(where: { isInstalled($0, in: installed) }) { return found }
        for candidate in candidates where await install(candidate) { return candidate }
        return installed.first
    }

    /// Where to transcribe `language`: the candidate in it (downloaded now if need be), else an installed locale in it
    /// (this Mac's region's first).
    static func locale(for language: String, among candidates: [Locale]) async -> Locale? {
        let installed = await SpeechTranscriber.installedLocales
        if let candidate = candidates.first(where: { code($0) == language }) {
            if isInstalled(candidate, in: installed) { return candidate }
            if await install(candidate) { return candidate }
        }
        let region = Locale.current.region
        return installed.first { code($0) == language && $0.region == region }
            ?? installed.first { code($0) == language }
    }

    private static func isInstalled(_ locale: Locale, in installed: [Locale]) -> Bool {
        installed.contains { $0.identifier(.bcp47) == locale.identifier(.bcp47) }
    }

    private static let attempted = Attempts()

    /// Downloads a language's model, once a process, waiting a minute at most (it goes on downloading after that, for
    /// the next recordings). False when it isn't installed by then.
    static func install(_ locale: Locale) async -> Bool {
        guard attempted.claim(locale.identifier(.bcp47)) else { return false }
        let transcriber = SpeechTranscriber(locale: locale, transcriptionOptions: [], reportingOptions: [],
                                            attributeOptions: [])
        let download = Task { () -> Bool in
            do {
                try await AssetInventory.assetInstallationRequest(supporting: [transcriber])?.downloadAndInstall()
                return true
            } catch {
                return false
            }
        }
        return await withCheckedContinuation { continuation in
            let once = Once()
            Task {
                let installed = await download.value
                once.run { continuation.resume(returning: installed) }
            }
            Task {
                try? await Task.sleep(for: .seconds(60))
                once.run { continuation.resume(returning: false) }
            }
        }
    }

    private final class Attempts: @unchecked Sendable {
        private let lock = NSLock()
        private var tried = Set<String>()

        func claim(_ key: String) -> Bool { lock.withLock { tried.insert(key).inserted } }
    }

    private final class Once: @unchecked Sendable {
        private let lock = NSLock()
        private var done = false

        func run(_ body: () -> Void) {
            let first = lock.withLock {
                defer { done = true }
                return !done
            }
            if first { body() }
        }
    }
}

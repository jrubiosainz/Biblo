import Foundation
import Testing
@testable import BibloKit

/// What's said in recordings: lines of about a sentence, how listening is noted, and the listening pass over recordings
/// indexed before transcription came.
@Suite final class SpeechTests {
    /// In Caches, not the temporary folder: the crawl reports /private/var/… for /var/… (see `LongFilesTests`).
    let folder: URL = {
        let caches = FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask)[0]
        let url = caches.appendingPathComponent("BibloTests-\(UUID().uuidString)")
        try? FileManager.default.createDirectory(at: url, withIntermediateDirectories: true)
        return url
    }()

    deinit {
        try? FileManager.default.removeItem(at: folder)
    }

    var files: URL { folder.appendingPathComponent("files") }

    func store() throws -> IndexStore { try IndexStore(directory: folder.appendingPathComponent("index")) }

    /// Words as the transcriber writes them (each with the space before it), `step` seconds apart from `start`.
    func words(_ text: String, from start: Double, step: Double = 0.4, confidence: Double? = 0.9) -> [Speech.Word] {
        text.split(separator: " ").enumerated().map { index, word in
            let begin = start + Double(index) * step
            return Speech.Word(start: begin, end: begin + step * 0.8, text: " " + word, confidence: confidence)
        }
    }

    // MARK: Lines

    @Test func sentencesBecomeLines() {
        let lines = Speech.lines(words("Good morning everyone.", from: 0)
            + words("Today we look at the third quarter results for the northern region.", from: 1.4)
            + words("Revenue grew by twelve percent.", from: 8)     // after a pause of almost 2 s
            + words("Exactly.", from: 10.2))
        #expect(lines.map(\.text) == [
            "Good morning everyone. Today we look at the third quarter results for the northern region.",
            "Revenue grew by twelve percent. Exactly.",
        ])
        #expect(lines.map(\.start) == [0, 8])
        #expect(abs(lines[1].end - 10.52) < 0.001)
    }

    @Test func pausesAndLongRunsEndLines() {
        let paused = Speech.lines(words("so the plan is simple", from: 0)
            + words("we ship on friday and review on monday", from: 4))
        #expect(paused.map(\.text) == ["so the plan is simple", "we ship on friday and review on monday"])

        func counts(_ lines: [SpokenLine]) -> [Int] { lines.map { $0.text.split(separator: " ").count } }
        let fifty = (1...50).map { "word\($0)" }.joined(separator: " ")
        #expect(counts(Speech.lines(words(fifty, from: 0, step: 0.3))) == [40, 10])     // 40 words at most
        let thirty = (1...30).map { "word\($0)" }.joined(separator: " ")
        #expect(counts(Speech.lines(words(thirty, from: 0, step: 1))) == [21, 9])       // 20 seconds at most
    }

    @Test func unsureLinesAreLeftOut() {
        let lines = Speech.lines(words("la la la la la la la la", from: 0, confidence: 0.2)
            + words("Thanks for joining the call.", from: 5)
            + words("See you next week.", from: 10, confidence: nil))
        #expect(lines.map(\.text) == ["Thanks for joining the call.", "See you next week."])
    }

    @Test func listeningIsNotedInInfo() {
        var info = ["duration": "62"]
        Heard.off.note(in: &info)
        #expect(info == ["duration": "62"])
        Heard.unavailable.note(in: &info)       // not listened to: the next process tries again
        #expect(info == ["duration": "62", "speech": "unavailable"])
        Heard.said([SpokenLine(start: 0, end: 2, text: "Hola a todos.")], language: "es_ES").note(in: &info)
        #expect(info == ["duration": "62", "speech": "es_ES", "speech_version": Speech.version])
        Heard.nothing.note(in: &info)
        #expect(info["speech"] == "none" && info["speech_version"] == Speech.version)
        Heard.unreadable.note(in: &info)
        #expect(info["speech"] == "unreadable")
    }

    // MARK: The index

    @Test func unheardRecordingsAndTheirSpeech() throws {
        let store = try store()
        var ids: [String: Int64] = [:]
        for (inode, (path, kind)) in [("/m/talk.m4a", FileKind.audio), ("/m/clip.mov", .video), ("/m/photo.png", .image),
                                      ("/m/new.m4a", .audio)].enumerated() {
            ids[path] = try store.insert(Candidate(path: path, kind: kind, size: 10, mtime: 1, inode: UInt64(inode + 1),
                                                   device: 1))
        }
        let talk = ids["/m/talk.m4a"]!
        try store.finish(talk, state: "done", info: ["duration": "60"])
        try store.finish(ids["/m/clip.mov"]!, state: "done", info: ["speech": "en_US", "speech_version": Speech.version])
        try store.finish(ids["/m/photo.png"]!, state: "done")
        #expect(try store.unheard(version: Speech.version).map(\.path) == ["/m/talk.m4a"])   // not pending ones
        #expect(try store.unheard(version: "0").map(\.path).sorted() == ["/m/clip.mov", "/m/talk.m4a"])
        store.scope = ["/elsewhere"]
        #expect(try store.unheard(version: Speech.version).isEmpty)
        store.scope = nil

        // What was said goes, the sound windows and the name stay.
        try store.addSegment(file: talk, kind: .audio, modality: .audio, loc: 0, locEnd: 30,
                             vector: FakeEmbedder.vector(for: "sound"))
        try store.addSegment(file: talk, kind: .speech, modality: .text, loc: 3, locEnd: 7, excerpt: "a quokka smiles",
                             text: "a quokka smiles", vector: FakeEmbedder.vector(for: "a quokka smiles"))
        try store.deleteSegments(of: talk, kind: .speech)
        var kinds: [String] = []
        try store.db.query("SELECT kind FROM segments WHERE file = ? ORDER BY kind", [.int(talk)]) {
            kinds.append($0.text(0) ?? "")
        }
        #expect(kinds == ["audio", "name"])
        var quokkas = -1
        try store.db.query("SELECT COUNT(*) FROM fts WHERE fts MATCH 'quokka'") { quokkas = Int($0.int(0)) }
        #expect(quokkas == 0)

        // Info is set only in the state it was listened to in.
        try store.setInfo(talk, ["speech": "none", "speech_version": Speech.version], ifState: "pending")
        #expect(try store.info(of: talk) == ["duration": "60"])
        try store.setInfo(talk, ["duration": "60", "speech": "none", "speech_version": Speech.version], ifState: "done")
        #expect(try store.info(of: talk)["speech"] == "none")
        #expect(try store.state(of: talk) == "done")
        #expect(try store.unheard(version: Speech.version).isEmpty)
    }

    // MARK: Listening, on this Mac (macOS 26)

    /// A recording of `text` said by `voice` (`say`), in `files`.
    func recording(_ name: String, saying text: String, voice: String = "Samantha") throws -> URL {
        try FileManager.default.createDirectory(at: files, withIntermediateDirectories: true)
        let url = files.appendingPathComponent(name)
        let say = Process()
        say.executableURL = URL(fileURLWithPath: "/usr/bin/say")
        say.arguments = ["-v", voice, "-o", url.path, text]
        try say.run()
        say.waitUntilExit()
        #expect(say.terminationStatus == 0)
        return url
    }

    /// The `speech` segments stored, in order: when, and what's said.
    func said(_ store: IndexStore) throws -> [(loc: Double, text: String)] {
        var out: [(Double, String)] = []
        try store.db.query("SELECT loc, excerpt FROM segments WHERE kind = 'speech' ORDER BY loc") {
            out.append(($0.double(0), $0.text(1) ?? ""))
        }
        return out
    }

    /// Where keyword search finds `word`: the segment's kind and place.
    func found(_ store: IndexStore, _ word: String) throws -> [(kind: String, loc: Double)] {
        var out: [(String, Double)] = []
        try store.db.query("""
            SELECT s.kind, s.loc FROM fts JOIN segments s ON s.id = fts.rowid WHERE fts MATCH ? ORDER BY s.loc
            """, [.text("\"\(word)\"")]) { out.append(($0.text(0) ?? "", $0.isNull(1) ? -1 : $0.double(1))) }
        return out
    }

    func count(_ store: IndexStore, kind: SegmentKind) throws -> Int {
        var count = 0
        try store.db.query("SELECT COUNT(*) FROM segments WHERE kind = ?", [.text(kind.rawValue)]) {
            count = Int($0.int(0))
        }
        return count
    }

    static let briefing = "Welcome to the weekly briefing. The warehouse in Rotterdam shipped four thousand pallets "
        + "last week, a new record for the team. Our next review with the finance department is on Thursday morning."

    @Test(.enabled(if: Speech.isAvailable)) func recordingsIndexedBeforeAreListenedTo() throws {
        let url = try recording("Weekly briefing.aiff", saying: Self.briefing)
        let store = try store()
        let embedder = FakeEmbedder()
        var deaf = IndexOptions()
        deaf.speech = false
        let before = try Indexer(store: store, options: deaf, makeEmbedder: { embedder })
        _ = try before.sync([files])
        #expect(try before.run() == ["done": 1])
        #expect(try before.unheard().isEmpty)        // listening is off
        #expect(try said(store).isEmpty)
        let sounds = try count(store, kind: .audio)
        #expect(sounds > 0)

        // Turned on (it doesn't change the fingerprint: nothing is indexed again), it listens to what was indexed.
        let indexer = try Indexer(store: store, options: IndexOptions(), makeEmbedder: { embedder })
        #expect(try indexer.unheard().map(\.path) == [url.path])
        let embedded = embedder.texts
        var events: [Indexer.Event] = []
        #expect(try indexer.listen(onEvent: { events.append($0) }) == ["heard": 1])
        #expect(events.map(\.state) == ["heard"])
        #expect(events.first?.note?.contains("spoken lines (en_") == true)
        let lines = try said(store)
        #expect(lines.count >= 2)
        #expect(embedder.texts - embedded == lines.count)     // the lines alone
        #expect(lines.map(\.text).joined(separator: " ").lowercased().contains("warehouse"))
        // Keyword search finds the moment it's said, past the first line.
        let thursday = try found(store, "thursday")
        #expect(thursday.map(\.kind) == ["speech"])
        #expect((thursday.first?.loc ?? 0) > 3)
        #expect(try count(store, kind: .audio) == sounds)    // its sound windows stay
        var info: [String: String] = [:]
        try store.db.query("SELECT info FROM files WHERE path = ?", [.text(url.path)]) { row in
            info = (try? JSONSerialization.jsonObject(with: Data((row.text(0) ?? "{}").utf8)) as? [String: String]) ?? [:]
        }
        #expect(info["speech"]?.hasPrefix("en_") == true && info["speech_version"] == Speech.version)
        #expect(try indexer.unheard().isEmpty)
        #expect(try indexer.listen().isEmpty)
    }

    @Test(.enabled(if: Speech.isAvailable)) func newRecordingsAreHeardAsTheyreIndexed() throws {
        _ = try recording("Weekly briefing.aiff", saying: Self.briefing)
        _ = try recording("Hum.aiff", saying: "[[slnc 4000]]")      // nothing said: skipped as silent
        let store = try store()
        let indexer = try Indexer(store: store, options: IndexOptions(), makeEmbedder: { FakeEmbedder() })
        _ = try indexer.sync([files])
        var notes: [String: String] = [:]
        let states = try indexer.run(onEvent: { notes[($0.path as NSString).lastPathComponent] = $0.note ?? "" })
        #expect(states["done"] == 1)
        #expect(notes["Weekly briefing.aiff"]?.contains("spoken lines (en_") == true)
        #expect(try said(store).count >= 2)
        #expect(try indexer.unheard().isEmpty)
    }
}

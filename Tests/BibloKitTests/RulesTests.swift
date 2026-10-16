import Foundation
import Testing
@testable import BibloKit

@Suite struct RulesTests {
    let folder: URL = {
        let url = FileManager.default.temporaryDirectory.appendingPathComponent("BibloTests-\(UUID().uuidString)")
        try? FileManager.default.createDirectory(at: url, withIntermediateDirectories: true)
        return url
    }()

    @Test func typeScriptIsNotVideo() throws {
        let file = folder.appendingPathComponent("app.ts")
        try "export const x: number = 1;\n".write(to: file, atomically: true, encoding: .utf8)
        #expect(Rules.classify(file, type: .init(filenameExtension: "ts"), options: IndexOptions()) == .skip("code or data file"))
    }

    @Test func realTransportStreamIsVideo() throws {
        var bytes = [UInt8](repeating: 0xFF, count: 188 * 4)
        for packet in 0..<4 { bytes[packet * 188] = 0x47 }
        let file = folder.appendingPathComponent("clip.ts")
        try Data(bytes).write(to: file)
        #expect(Rules.classify(file, type: .init(filenameExtension: "ts"), options: IndexOptions()) == .index(.video))
    }

    @Test func codeCanBeIncluded() {
        var options = IndexOptions()
        options.includeCode = true
        let file = folder.appendingPathComponent("main.py")
        #expect(Rules.classify(file, type: .init(filenameExtension: "py"), options: options) == .index(.doc))
    }

    @Test func machineNames() {
        #expect(Rules.looksMachineNamed("clip_000123"))
        #expect(Rules.looksMachineNamed("frame-0042"))
        #expect(Rules.looksMachineNamed("3f9a1c0e-12ab-4cde"))
        #expect(Rules.looksMachineNamed("000123"))
        #expect(!Rules.looksMachineNamed("IMG_1234"))
        #expect(!Rules.looksMachineNamed("PXL_20260101_123456789"))
        #expect(!Rules.looksMachineNamed("Screenshot 2026-10-01 at 9.41.07 PM"))
        #expect(!Rules.looksMachineNamed("Tokyo itinerary"))
    }

    @Test func datasetNeedsManyMachineNamedFiles() {
        let clips = (0..<400).map { (folder: "/x/clips", stem: String(format: "clip_%06d", $0), kind: FileKind.audio) }
        let photos = (0..<400).map { (folder: "/x/camera", stem: "IMG_\(1000 + $0)", kind: FileKind.image) }
        let few = (0..<50).map { (folder: "/x/few", stem: "clip_\($0)", kind: FileKind.audio) }
        let datasets = Rules.datasetFolders(clips + photos + few, roots: [])
        #expect(datasets == ["/x/clips": 400])
    }

    @Test func ftsQueryDropsStopwordsAndKindWords() {
        #expect(Searcher.ftsQuery("the screenshot of my payment error") == "\"payment\" OR \"error\"")
        #expect(Searcher.ftsQuery("zebr", prefixLast: true) == "\"zebr\"*")
        #expect(Searcher.ftsQuery("a screenshot") == nil)
    }

    @Test func chunksOverlapAndRespectWords() {
        let text = (1...600).map { "word\($0)" }.joined(separator: " ")
        let chunks = DocExtractor.chunks(text, size: 500, overlap: 100, limit: 100)
        #expect(chunks.count > 5)
        #expect(chunks.allSatisfy { $0.count <= 500 })
        #expect(chunks.allSatisfy { $0.hasPrefix("word") })   // never starts mid-word
        #expect(chunks.last?.hasSuffix("word600") == true)
    }

    @Test func htmlBecomesPlainText() {
        let html = """
            <html><head><title>T</title><style>p { color: red }</style></head>
            <body><h1>Trip &amp; plans</h1><p>Fly to <b>Tokyo</b>&nbsp;on Friday.</p><script>var x = 1;</script>
            <p>Caf&#233; &#x2014; ramen</p><!-- hidden --></body></html>
            """
        #expect(DocExtractor.plainText(fromHTML: html) == "Trip & plans\nFly to Tokyo on Friday.\nCafé — ramen")
    }

    @Test func halfVectorsConvertBackExactly() throws {
        let vector = (0..<Vectors.dimension).map { Float(sin(Double($0) * 0.37)) * 0.05 }
        let storage = try #require(VectorStorage(rows: 2))
        Vectors.half(vector).copyBytes(to: UnsafeMutableRawBufferPointer(start: storage.halves + Vectors.dimension,
                                                                         count: Vectors.dimension * 2))
        Vectors.floats(fromHalf: storage.halves, count: Vectors.dimension * 2, to: storage.block)
        let back = Array(UnsafeBufferPointer(start: storage.block + Vectors.dimension, count: Vectors.dimension))
        #expect(back == vector.map { Float(Float16($0)) })
        #expect(storage.block[0] == 0)   // fresh mmap'd memory is zeroed, and row 0 was left alone
    }

    @Test func meaningTakesOutEachModalitysLevelOnOneScale() {
        // Text scores sit higher than image scores here: that level comes out. The spread is shared, so a modality
        // whose scores are bunched up doesn't get its best ones inflated: 0.01 above average beats 0.002 above, 5:1.
        let text: [Float] = (0..<30).map { 0.70 + Float($0 % 3) * 0.01 }
        let image: [Float] = (0..<30).map { 0.55 + Float($0 % 3) * 0.002 }
        let scores = text + image
        let modality = Array(repeating: Modality.text, count: 30) + Array(repeating: Modality.image, count: 30)
        let z = Searcher.meaning(scores, modality)
        #expect(abs(z[1]) < 1e-4 && abs(z[31]) < 1e-4)   // 0.71 and 0.552: each at its modality's average
        #expect(abs(z[2] / z[32] - 5) < 0.01)
        let means = Searcher.modalityMeans(scores, modality)
        #expect(abs(means[.text]! - 0.71) < 0.001 && abs(means[.image]! - 0.552) < 0.001)
        #expect(abs(means[.audio]! - 0.631) < 0.001)   // no audio vectors: the average of all
    }

    @Test func laterPagesAreScoredWithoutMovingTheScale() {
        // A long book's later pages, far from the query, would pull the text average down and lift all text.
        let scores: [Float] = (0..<30).map { 0.70 + Float($0 % 3) * 0.01 } + (0..<30).map { 0.55 + Float($0 % 3) * 0.002 }
        let modality = Array(repeating: Modality.text, count: 30) + Array(repeating: Modality.image, count: 30)
        let book: [Float] = (0..<400).map { 0.60 + Float($0 % 5) * 0.004 } + [0.80]   // one page that matches
        let z = Searcher.meaning(scores, modality)
        let withBook = Searcher.meaning(scores + book, modality + Array(repeating: .text, count: book.count),
                                        setsScale: Array(repeating: true, count: 60) + Array(repeating: false, count: 401))
        for row in 0..<60 { #expect(abs(z[row] - withBook[row]) < 1e-9) }
        #expect(withBook.last! > z.max()!)   // the matching page stands out on the same scale
    }

    @Test func codesAndLongNumbersAreLookups() {
        #expect(Searcher.isLookup(["k7q2lm"]))
        #expect(Searcher.isLookup(["trx50"]))
        #expect(Searcher.isLookup(["4815162342"]))
        #expect(Searcher.isLookup(["2041"]))
        #expect(!Searcher.isLookup(["417"]))           // too short to be an ID
        #expect(!Searcher.isLookup(["inv", "2041"]))    // a word in it
        #expect(!Searcher.isLookup([]))
    }

    @Test func weakerMatchesFoldBelowHalfTheTopScore() {
        func hit(_ score: Double) -> SearchHit {
            SearchHit(path: "/\(score)", kind: .image, score: score, z: nil, cosine: nil, keywordRank: nil, segment: .image,
                      segmentID: 1, loc: nil, locEnd: nil, excerpt: nil, modified: 0, size: 0, info: [:])
        }
        #expect(Searcher.strongCount([hit(6), hit(4.1), hit(3), hit(2.9), hit(0.7)]) == 3)
        #expect(Searcher.strongCount([hit(0.71)]) == 1)
        #expect(Searcher.strongCount([]) == 0)
    }

    @Test func nestedRootsAreCrawledOnce() throws {
        let inner = folder.appendingPathComponent("inner")
        try FileManager.default.createDirectory(at: inner, withIntermediateDirectories: true)
        try Data("notes about the trip".utf8).write(to: inner.appendingPathComponent("trip.txt"))
        let report = Crawler.crawl([folder, inner], options: IndexOptions())
        #expect(report.candidates.map { ($0.path as NSString).lastPathComponent } == ["trip.txt"])
    }

    @Test func officeLockFilesAreLeftOut() throws {
        let lock = folder.appendingPathComponent("~$Q3 review.pptx")
        try Data("jesus rubio".utf8).write(to: lock)
        #expect(Rules.classify(lock, type: .init(filenameExtension: "pptx"), options: IndexOptions())
                == .skip("Office lock file"))
        #expect(!Rules.mayBeIndexed("~$Q3 review.pptx", options: IndexOptions()))
        #expect(Rules.mayBeIndexed("Q3 review.pptx", options: IndexOptions()))
    }

    @Test func documentsAreDecksWordDocumentsAndPDFs() {
        let documents = ["Q3 review.pptx", "Brief.docx", "Old brief.doc", "Contract.PDF", "Notes.rtf", "Draft.odt"]
        let others = ["~$Brief.docx", "chart.png", "README.md", "events.jsonl", "Budget.xlsx", "main.swift", "Deck"]
        #expect(documents.filter { !Rules.isDocument($0, options: IndexOptions()) } == [])
        #expect(others.filter { Rules.isDocument($0, options: IndexOptions()) } == [])
        var noPDFs = IndexOptions()
        noPDFs.excludedExtensions = IndexOptions.extensions("pdf")
        #expect(!Rules.isDocument("Contract.pdf", options: noPDFs))
    }

    @Test func documentsOnlyFolderKeepsOnlyDocuments() throws {
        // As the Copilot app leaves a session: what it made, its own files, and the project it made a deck with.
        let made = folder.appendingPathComponent("session/files")
        let project = folder.appendingPathComponent("session/deck")
        try FileManager.default.createDirectory(at: made, withIntermediateDirectories: true)
        try FileManager.default.createDirectory(at: project.appendingPathComponent("out"),
                                                withIntermediateDirectories: true)
        for name in ["Q3 review.pptx", "Brief.docx", "Contract.pdf", "~$Brief.docx", "chart.png", "notes.md",
                     "events.jsonl"] {
            try Data("x".utf8).write(to: made.appendingPathComponent(name))
        }
        try Data("{}".utf8).write(to: project.appendingPathComponent("package.json"))
        try Data("x".utf8).write(to: project.appendingPathComponent("out/Launch.pptx"))
        var options = IndexOptions()
        options.documentOnlyFolders = [folder.path]
        let report = Crawler.crawl([folder], options: options)
        #expect(report.candidates.map { ($0.path as NSString).lastPathComponent }.sorted()
                == ["Brief.docx", "Contract.pdf", "Launch.pptx", "Q3 review.pptx"])
        #expect(report.projectRoots.isEmpty)   // it counts as any folder there: the watcher mustn't leave it out
        #expect(report.skipped["not a document (documents-only folder)"] == 5)
        // Chosen as any other folder, it keeps the rest too.
        let whole = Crawler.crawl([folder], options: IndexOptions())
        #expect(whole.candidates.contains { $0.path.hasSuffix("/notes.md") })
    }

    @Test func documentsOnlyFolderLeavesOutCrowdedProjects() throws {
        // A repo cloned in a session, with the test corpus it makes: more documents than anyone made there.
        let made = folder.appendingPathComponent("session/files")
        let poc = made.appendingPathComponent("rag-poc")
        try FileManager.default.createDirectory(at: poc.appendingPathComponent("corpus/out"),
                                                withIntermediateDirectories: true)
        try FileManager.default.createDirectory(at: poc.appendingPathComponent("web"), withIntermediateDirectories: true)
        try Data("x".utf8).write(to: poc.appendingPathComponent("requirements.txt"))
        try Data("{}".utf8).write(to: poc.appendingPathComponent("web/package.json"))   // the outermost project counts
        try Data("x".utf8).write(to: poc.appendingPathComponent("web/Guide.pdf"))
        for n in 1...Rules.projectDocumentLimit {   // with the guide, one too many
            try Data("x".utf8).write(to: poc.appendingPathComponent("corpus/out/Policy \(n).pdf"))
        }
        try Data("x".utf8).write(to: made.appendingPathComponent("Proposal.docx"))
        try Data("{}".utf8).write(to: folder.appendingPathComponent("package.json"))   // the chosen folder is no project
        var options = IndexOptions()
        options.documentOnlyFolders = [folder.path]
        let report = Crawler.crawl([folder], options: options)
        #expect(report.candidates.map { ($0.path as NSString).lastPathComponent } == ["Proposal.docx"])
        #expect(report.skipped["in a code project with too many documents"] == Rules.projectDocumentLimit + 1)
        #expect(report.projectRoots.map { ($0 as NSString).lastPathComponent } == ["rag-poc"])
    }
}

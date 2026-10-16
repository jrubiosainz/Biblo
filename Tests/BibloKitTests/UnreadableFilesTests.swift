import Foundation
import Testing
@testable import BibloKit

/// Documents that can't be read: empty ones, and ones encrypted by a sensitivity label (or a password). Indexing tells
/// them apart; search finds them by their name.
@Suite final class UnreadableFilesTests {
    /// In Caches, not the temporary folder: the walk reports /private/var/… for /var/… (see `LongFilesTests`).
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

    @Test func emptyAndEncryptedDocumentsAreToldApart() throws {
        try FileManager.default.createDirectory(at: files, withIntermediateDirectories: true)
        // An encrypted Office document is an OLE file holding the encrypted package.
        let encrypted = Data([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1] + [UInt8](repeating: 0, count: 600))
        try Data().write(to: files.appendingPathComponent("Empty.docx"))
        try Data().write(to: files.appendingPathComponent("Empty.pptx"))
        try encrypted.write(to: files.appendingPathComponent("Labelled.docx"))
        try encrypted.write(to: files.appendingPathComponent("Labelled.pptx"))
        try Data("jesus rubio".utf8).write(to: files.appendingPathComponent("~$Labelled.docx"))
        try "Notes from the harbour meeting".write(to: files.appendingPathComponent("Notes.txt"), atomically: true,
                                                   encoding: .utf8)
        let store = try store()
        let embedder = FakeEmbedder()
        let indexer = try Indexer(store: store, options: IndexOptions(), makeEmbedder: { embedder })
        _ = try indexer.sync([files])
        #expect(try indexer.run() == ["done": 1, "skipped": 2, "failed": 2])
        var state: [String: String] = [:], detail: [String: String] = [:]
        try store.db.query("SELECT path, state, detail FROM files") { row in
            let name = ((row.text(0) ?? "") as NSString).lastPathComponent
            state[name] = row.text(1)
            detail[name] = row.text(2)
        }
        // Not the lock file: a few bytes saying who has the document open.
        #expect(state == ["Empty.docx": "skipped", "Empty.pptx": "skipped", "Labelled.docx": "failed",
                          "Labelled.pptx": "failed", "Notes.txt": "done"])
        #expect(detail["Empty.docx"] == "empty file")
        #expect(detail["Empty.pptx"] == "empty file")
        #expect(detail["Labelled.docx"] == "encrypted (a sensitivity label or a password)")
        #expect(detail["Labelled.pptx"] == "encrypted (a sensitivity label or a password)")
    }

    @Test func aNameStandsInForWhatCantBeRead() throws {
        let store = try store()
        var inode: UInt64 = 0
        /// A document, read (its text and the text's vector) or not (encrypted: only its name).
        func add(_ path: String, text: String? = nil, vector: [Float]? = nil) throws {
            inode += 1
            let id = try store.insert(Candidate(path: path, kind: .doc, size: 10, mtime: 1, inode: inode, device: 1))
            if let text {
                try store.addSegment(file: id, kind: .chunk, modality: .text, loc: 1, text: text, vector: vector)
                try store.finish(id, state: "done")
            } else {
                try store.finish(id, state: "failed", detail: "encrypted (a sensitivity label or a password)")
            }
        }
        /// A unit vector `share` of the way from a vector of its own to `query`.
        func near(_ query: [Float], _ share: Float, seed: String) -> [Float] {
            let mixed = zip(query, FakeEmbedder.vector(for: seed)).map { share * $0 + (1 - share) * $1 }
            let norm = mixed.reduce(0) { $0 + $1 * $1 }.squareRoot()
            return mixed.map { $0 / norm }
        }
        let query = FakeEmbedder.vector(for: "citadel explained")
        for index in 1...60 {
            try add("/notes/Minutes \(index).txt", text: "Minutes of the harbour meeting \(index)",
                    vector: FakeEmbedder.vector(for: "minutes \(index)"))
        }
        try add("/notes/Citadel explained.md", text: "Citadel explained: how the platform keeps its agents in line",
                vector: near(query, 0.9, seed: "explainer"))
        for index in 1...3 {
            try add("/notes/Weekly \(index).md", text: "We spoke about Citadel again on Tuesday \(index)",
                    vector: near(query, 0.5, seed: "weekly \(index)"))
        }
        try add("/decks/citadel-explained.pptx")
        try add("/Citadel explained/old notes.pptx")   // the words are its folder's
        try add("/decks/citadel.pptx")   // one of the two

        let hits = try Searcher(store: store).search("citadel explained", queryVector: query)
        let names = hits.map { ($0.path as NSString).lastPathComponent }
        // Just under the one that explains it, over the ones that only mention it.
        #expect(Array(names.prefix(2)) == ["Citadel explained.md", "citadel-explained.pptx"])
        #expect(Set(names.dropFirst(2).prefix(3)) == ["Weekly 1.md", "Weekly 2.md", "Weekly 3.md"])
        #expect(Array(names.dropFirst(5)) == ["old notes.pptx", "citadel.pptx"])
        let deck = try #require(hits.first { $0.path == "/decks/citadel-explained.pptx" })
        #expect(deck.z == nil && !deck.byMeaning && deck.segment == .name)   // "Matches its name"
    }
}

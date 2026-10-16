import BibloKit
import Foundation

/// What to index, where the index and the model live, and the hotkey.
///
/// Saved in the app's defaults domain (com.jrubiosainz.Biblo). Launch arguments override any of it without being
/// saved, which is how tests point the app at the testbed and never at real folders:
///
///     Biblo.app/Contents/MacOS/Biblo -roots ~/BibloTestbed/real -indexDir <repo>/.dev/app-index \
///         -modelsDir <repo>/.dev/models -defaultsSuite com.jrubiosainz.Biblo.dev
///
/// `-roots` takes one folder, several joined with ":", or a plist array. `-defaultsSuite` keeps what the app saves
/// (onboarding's folders, a new hotkey) out of the real settings. With no roots the app indexes nothing and opens
/// onboarding: a fresh install never starts reading someone's home folder on its own.
///
/// Demo mode (`demoMode`, switched in Settings → General) swaps the folders for the sample files (`DemoFiles`) and the
/// index for one of their own, next to the real one; the saved folders stay as they were, untouched until it's off.
///
/// `copilotDocuments` (Settings → Folders) also searches the decks, Word documents and PDFs GitHub Copilot makes in the
/// hidden ~/.copilot. It's on by default, but off with `-defaultsSuite` unless `-copilotDocuments YES` turns it on, so
/// a test run never reads it.
nonisolated struct AppSettings: Sendable {
    var roots: [URL]
    /// Folders inside the roots that are never indexed.
    var excludedFolders: [URL]
    /// File extensions that are never indexed ("heic", "txt"), on top of what Biblo never reads anyway.
    var excludedTypes: [String]
    var indexDirectory: URL
    /// Where the model files are downloaded to and loaded from (the helpers get it as BIBLO_MODELS).
    var modelsDirectory: URL
    var hotkey: String
    /// On (the default), the big first pass of a folder (the backfill) runs on battery too; off, it waits for a
    /// charger. New files always index right away, and Low Power Mode or a hot Mac make the backfill wait either way.
    var indexOnBattery: Bool
    /// The query encoder (~0.25 GB) exits after this long without a query; the next panel open starts it again.
    var encoderIdleSeconds: Double
    /// Onboarding was finished (or closed after choosing folders); it doesn't open by itself again.
    var onboarded: Bool
    /// Code search: the folders whose code goes into the code index (none: code search is off), and the folders
    /// skipped in them (`FolderSelection`'s rule, as for `roots`). Searched with "code:" only.
    var codeRoots: [URL]
    var codeExcluded: [URL]
    /// The bundle id of the editor code results open in ("" for each file's default app); nil until one is chosen
    /// (`CodeEditor.chosen`).
    var codeEditor: String?
    /// The code index catches up once the code folders have been quiet this long (`-codeQuietSeconds`, default 60).
    var codeQuietSeconds: Double
    /// Searching the sample files instead of your folders (`demo`).
    var demoMode: Bool
    /// Documents made with GitHub Copilot are searched too (`documentFolders`).
    var copilotDocuments: Bool

    static let supportDirectory = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent("Library/Application Support/Biblo")
    static let defaultIndexDirectory = supportDirectory.appendingPathComponent("index.noindex")
    static let defaultHotkey = "cmd+shift+space"

    /// Demo mode, as this launch runs it: Settings saves a change for the next launch and relaunches, since the
    /// engine's folders and index are set when it starts. While it's on, nothing about folders is saved.
    static let demo = defaults.bool(forKey: "demoMode")

    /// The battery switch, in onboarding and Settings.
    static let batteryTitle = "Index on battery power"
    static let batteryDetail = "When it's off, a folder's first pass waits for a charger. New files always go in right away."

    /// Where settings are saved. Reads see launch arguments first either way. (UserDefaults is thread-safe.)
    nonisolated(unsafe) static let defaults: UserDefaults = {
        guard let suite = UserDefaults.standard.string(forKey: "defaultsSuite"), !suite.isEmpty,
              let defaults = UserDefaults(suiteName: suite) else { return .standard }
        return defaults
    }()

    static func load() -> AppSettings {
        let defaults = Self.defaults
        var settings = AppSettings(
            roots: folders(defaults, "roots"),
            excludedFolders: folders(defaults, "excludedFolders"),
            excludedTypes: (defaults.stringArray(forKey: "excludedTypes")
                ?? defaults.string(forKey: "excludedTypes").map { [$0] } ?? [])
                .flatMap { IndexOptions.extensions($0) }.sorted(),
            indexDirectory: defaults.string(forKey: "indexDir").map(folderURL) ?? defaultIndexDirectory,
            modelsDirectory: defaults.string(forKey: "modelsDir").map(folderURL) ?? ModelFiles.installed,
            hotkey: defaults.string(forKey: "hotkey") ?? defaultHotkey,
            indexOnBattery: defaults.object(forKey: "indexOnBattery") == nil || defaults.bool(forKey: "indexOnBattery"),
            encoderIdleSeconds: defaults.object(forKey: "encoderIdleSeconds") == nil
                ? 600 : max(1, defaults.double(forKey: "encoderIdleSeconds")),
            onboarded: defaults.bool(forKey: "onboarded"),
            codeRoots: folders(defaults, "codeRoots"),
            codeExcluded: folders(defaults, "codeExcludedFolders"),
            codeEditor: defaults.string(forKey: "codeEditor"),
            codeQuietSeconds: defaults.object(forKey: "codeQuietSeconds") == nil
                ? 60 : max(1, defaults.double(forKey: "codeQuietSeconds")),
            demoMode: demo,
            copilotDocuments: !demo && (defaults.object(forKey: "copilotDocuments") == nil
                ? UserDefaults.standard.string(forKey: "defaultsSuite") == nil
                : defaults.bool(forKey: "copilotDocuments")))
        if demo {
            // The samples' code goes to the code index only, as code in a chosen folder would.
            settings.roots = [DemoFiles.folder]
            settings.excludedFolders = [DemoFiles.code]
            settings.excludedTypes = []
            settings.codeRoots = [DemoFiles.code]
            settings.codeExcluded = []
            settings.onboarded = true
            settings.indexDirectory = settings.indexDirectory.deletingLastPathComponent()
                .appendingPathComponent("demo.noindex")
        }
        return settings
    }

    /// A list of folders: a plist array, or paths joined with ":" (the form launch arguments use).
    private static func folders(_ defaults: UserDefaults, _ key: String) -> [URL] {
        let paths: [String]
        if let list = defaults.stringArray(forKey: key) {
            paths = list
        } else if let joined = defaults.string(forKey: key) {
            paths = joined.split(separator: ":").map(String.init)
        } else {
            paths = []
        }
        var seen = Set<String>()
        return paths.filter { !$0.isEmpty }.map(folderURL).filter { seen.insert($0.path).inserted }
    }

    static func save(roots: [URL]) {
        guard !demo else { return }
        defaults.set(roots.map(\.path), forKey: "roots")
    }

    static func save(excludedFolders: [URL]) {
        guard !demo else { return }
        defaults.set(excludedFolders.map(\.path), forKey: "excludedFolders")
    }

    static func save(excludedTypes: [String]) {
        guard !demo else { return }
        defaults.set(excludedTypes, forKey: "excludedTypes")
    }

    static func save(hotkey: String) {
        defaults.set(hotkey, forKey: "hotkey")
    }

    static func save(indexOnBattery: Bool) {
        defaults.set(indexOnBattery, forKey: "indexOnBattery")
    }

    static func saveOnboarded() {
        guard !demo else { return }
        defaults.set(true, forKey: "onboarded")
    }

    static func save(codeRoots: [URL], excluded: [URL]) {
        guard !demo else { return }
        defaults.set(codeRoots.map(\.path), forKey: "codeRoots")
        defaults.set(excluded.map(\.path), forKey: "codeExcludedFolders")
    }

    static func save(codeEditor: String) {
        defaults.set(codeEditor, forKey: "codeEditor")
    }

    /// For the next launch (`demo`).
    static func save(demoMode: Bool) {
        defaults.set(demoMode, forKey: "demoMode")
    }

    static func save(copilotDocuments: Bool) {
        guard !demo else { return }
        defaults.set(copilotDocuments, forKey: "copilotDocuments")
    }

    /// Where GitHub Copilot (the app and the CLI) saves what it makes: each session's files, and each chat's.
    static let copilotFolders = ["~/.copilot/session-state", "~/.copilot/chats"].map(folderURL)

    /// The folders searched for their decks, Word documents and PDFs only (`IndexOptions.documentOnlyFolders`): the
    /// Copilot folders that are there, when `copilot` is on and no chosen folder searches them already. A hidden
    /// folder isn't walked, so a chosen home folder doesn't. None before folders are chosen (a fresh install reads
    /// nothing) or in demo mode.
    static func documentFolders(copilot: Bool, roots: [URL]) -> [URL] {
        guard copilot, !demo, !roots.isEmpty else { return [] }
        return copilotFolders.filter { folder in
            isFolder(folder) && !roots.contains { root in
                guard folder.path != root.path else { return true }
                guard FolderSelection.isInside(folder.path, root.path) else { return false }
                return !folder.path.dropFirst(root.path.count).split(separator: "/").contains { $0.hasPrefix(".") }
            }
        }
    }

    /// Expands "~" and resolves symlinks, so crawled paths match the paths FSEvents reports.
    static func folderURL(_ path: String) -> URL {
        URL(fileURLWithPath: (path.trimmingCharacters(in: .whitespaces) as NSString).expandingTildeInPath)
            .resolvingSymlinksInPath().standardizedFileURL
    }

    static func isFolder(_ url: URL) -> Bool {
        var isFolder: ObjCBool = false
        return FileManager.default.fileExists(atPath: url.path, isDirectory: &isFolder) && isFolder.boolValue
    }
}

/// "~/BibloTestbed/real" instead of "/Users/…/BibloTestbed/real".
nonisolated func tildePath(_ path: String) -> String {
    (path as NSString).abbreviatingWithTildeInPath
}

// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Biblo",
    platforms: [.macOS(.v14)],
    products: [
        .executable(name: "biblo", targets: ["biblo"]),
        .executable(name: "BibloApp", targets: ["BibloApp"]),
        .library(name: "BibloKit", targets: ["BibloKit"]),
    ],
    dependencies: [
        // In-app updates (the app only). build.sh embeds the framework in Contents/Frameworks and signs it.
        .package(url: "https://github.com/sparkle-project/Sparkle", exact: "2.10.0"),
    ],
    targets: [
        // The engine: crawler, extractors, index store, the embedder interface and worker client, search. No UI.
        .target(name: "BibloKit"),
        // llama.cpp (scripts/build-llama.sh builds it into Vendor/llama) and EmbeddingGemma 2 on it.
        .systemLibrary(name: "CLlama", path: "Sources/CLlama"),
        .target(
            name: "LlamaRuntime",
            dependencies: ["CLlama", "BibloKit"],
            linkerSettings: [.unsafeFlags(["-L\(Context.packageDirectory)/Vendor/llama/lib"])]
        ),
        // Developer CLI: estimate / index / search / status / eval. Doubles as the eval harness, and the app runs it as
        // its indexing helper and its query encoder.
        .executableTarget(name: "biblo", dependencies: ["BibloKit", "LlamaRuntime"]),
        // The menubar + hotkey app. build.sh wraps it into build.noindex/Biblo.app. (The product can't be called
        // "Biblo": on a case-insensitive disk it would collide with the `biblo` CLI binary.)
        .executableTarget(
            name: "BibloApp",
            dependencies: ["BibloKit", .product(name: "Sparkle", package: "Sparkle")],
            swiftSettings: [.defaultIsolation(MainActor.self)],
            linkerSettings: [.unsafeFlags(["-Xlinker", "-rpath", "-Xlinker", "@executable_path/../Frameworks"])]
        ),
        .testTarget(name: "BibloKitTests", dependencies: ["BibloKit"]),
        .testTarget(name: "LlamaRuntimeTests", dependencies: ["LlamaRuntime"]),
    ]
)

#!/bin/bash
# Makes demo mode's sample files, Resources/Demo.noindex: documents, slides, pictures, screenshots, audio, video and
# code about Microsoft Foundry, Fabric and Copilot, with public facts, fictitious companies and made-up numbers only.
# ./build.sh puts them in the app; Settings → General → Demo mode copies them to ~/Biblo Demo and searches only them.
# (".noindex": neither Spotlight nor Biblo reads them here, in the repo.)
# Only the hand-written files are in git (see .gitignore): first download the official logos into scripts/demo/assets,
# as its SOURCES.md says.
#
# The text and code files are written by hand and kept as they are. This makes everything else again (PDF, Word, RTF,
# PowerPoint, PNG, JPEG, M4A, MP4) with scripts/demo/make_demo.py: pictures are HTML drawn by a headless Edge or
# Chrome, voices are macOS's `say` or Azure AI Speech, videos ffmpeg, decks python-pptx, Word and RTF files textutil.
# macOS's voices are for personal, non-commercial use: samples you'll show in public, in a post or a talk, should speak
# with Azure AI Speech's neural voices (BIBLO_TTS=azure, with the key and region of any Speech or AI Services
# resource). Azure's takes are kept in ~/.cache/biblo-demo-tts, so a line sounds the same every time it's made; macOS's
# voices never say it quite the same way twice. Either way, after making audio or video again, check what Biblo hears
# in each one with `biblo listen <file>`.
#
#   scripts/make-demo.sh              everything
#   scripts/make-demo.sh slides …     only what's named (see make_demo.py --help)
#   BIBLO_TTS=azure AZURE_SPEECH_KEY=… AZURE_SPEECH_REGION=westeurope scripts/make-demo.sh audio videos more_audio more_videos
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
command -v ffmpeg >/dev/null || { echo "needs ffmpeg (brew install ffmpeg)" >&2; exit 1; }
VENV="$REPO/.dev/demo-venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --disable-pip-version-check python-pptx pillow pygments
fi
exec "$VENV/bin/python" "$REPO/scripts/demo/make_demo.py" "$@"

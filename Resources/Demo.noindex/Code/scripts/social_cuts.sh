#!/usr/bin/env bash
# Cuts a landscape video into the two shapes the social networks want: 9:16 for Reels, TikTok and Shorts, and 1:1 for
# LinkedIn and the Instagram feed. The cuts land next to the original:
#
#   ./social_cuts.sh "Trailhead 3 – teaser.mp4"       # "Trailhead 3 – teaser – 9x16.mp4" and "… – 1x1.mp4"
#   ./social_cuts.sh "Trailhead 3 – teaser.mp4" 15    # only the first 15 seconds
#
# 9:16 doesn't crop: the whole frame sits in the middle, over a blurred, darker copy of itself, so the tent never ends
# up out of the shot. 1:1 sits it on the brand's forest green.
#
# Most people watch with the sound off. If a subtitle file with the same name sits next to the video ("Trailhead 3 –
# teaser.srt"), it's burned in, under the picture. That needs an ffmpeg with libass: Homebrew's ffmpeg-full has it,
# plain ffmpeg doesn't. Point the script at it with
#
#   FFMPEG=/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg ./social_cuts.sh "Trailhead 3 – teaser.mp4"
#
# Embargo: nothing about Trailhead 3 goes out before Tuesday, November 3 at 9:00 CET, except the teaser, on Tuesday,
# October 27. Marta schedules every post: send her the cuts, don't post them yourself.

set -euo pipefail

ffmpeg=${FFMPEG:-ffmpeg}
if [[ $# -lt 1 || $# -gt 2 || ! -f ${1:-} ]]; then
  echo 'usage: social_cuts.sh VIDEO [SECONDS]' >&2
  exit 64
fi
seconds=${2:-}
if [[ -n $seconds && ! $seconds =~ ^[1-9][0-9]*$ ]]; then
  echo 'SECONDS is a whole number, like 15' >&2
  exit 64
fi
command -v "$ffmpeg" >/dev/null || { echo 'social_cuts.sh needs ffmpeg: brew install ffmpeg-full' >&2; exit 69; }

video="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
base=${video%.*}

# ffmpeg runs in a scratch folder: the subtitles filter can't take a path with quotes, colons or commas in it, so it
# reads a copy called subs.srt from there.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cd "$work"

subs_tall='' subs_square=''
if [[ -f $base.srt ]]; then
  filters=$("$ffmpeg" -hide_banner -filters 2>/dev/null)
  if [[ $filters == *' subtitles '* ]]; then
    cp "$base.srt" subs.srt
    style='FontName=Helvetica Neue,FontSize=12,Bold=1,Outline=1,Shadow=0'
    subs_tall=",subtitles=subs.srt:force_style='$style,MarginV=60'"
    subs_square=",subtitles=subs.srt:force_style='$style,MarginV=26'"
  else
    echo "warning: $ffmpeg can't burn in subtitles (it has no libass), so the cuts go without them" >&2
  fi
fi

render() {  # render SHAPE FILTERGRAPH
  local out="$base – $1.mp4"
  "$ffmpeg" -hide_banner -loglevel error -stats -y -i "$video" ${seconds:+-t "$seconds"} \
    -filter_complex "$2" -map '[v]' -map '0:a?' \
    -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k "$out"
  echo "Wrote $out"
}

render 9x16 "[0:v]split[a][b];\
[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20,eq=brightness=-0.1[bg];\
[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2$subs_tall[v]"
render 1x1 "[0:v]scale=1080:1080:force_original_aspect_ratio=decrease:force_divisible_by=2,\
pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=0x0e2118$subs_square[v]"

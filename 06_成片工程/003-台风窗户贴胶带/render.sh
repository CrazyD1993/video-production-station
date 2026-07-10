#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
FFMPEG="/opt/homebrew/bin/ffmpeg"
RAIN="$ROOT/../../04_素材库/视频素材/003-台风窗户贴胶带/003-01-rainy-window-mixkit.mp4"
CURTAIN="$ROOT/../../04_素材库/视频素材/003-台风窗户贴胶带/003-05-curtain-mixkit.mp4"

mkdir -p "$ROOT/clips" "$ROOT/work" "$ROOT/renders"

for slide in title fragment wind checklist end; do
  sips -s format png "$ROOT/slides/$slide.svg" --out "$ROOT/work/$slide.png" >/dev/null
done

say -v Tingting -r 120 -f "$ROOT/narration.txt" -o "$ROOT/work/narration.aiff"

"$FFMPEG" -y -stream_loop -1 -i "$RAIN" -loop 1 -i "$ROOT/work/title.png" -t 14 \
  -filter_complex "[0:v]scale=-2:1920,crop=1080:1920,setsar=1[bg];[bg][1:v]overlay=0:0" -r 30 -pix_fmt yuv420p \
  "$ROOT/clips/01-rain-window.mp4"

"$FFMPEG" -y -loop 1 -i "$ROOT/work/fragment.png" -t 13 -r 30 \
  -pix_fmt yuv420p "$ROOT/clips/02-fragment-diagram.mp4"

"$FFMPEG" -y -loop 1 -i "$ROOT/work/wind.png" -t 12 -r 30 \
  -pix_fmt yuv420p "$ROOT/clips/03-wind-diagram.mp4"

"$FFMPEG" -y -loop 1 -i "$ROOT/work/checklist.png" -t 18 -r 30 \
  -pix_fmt yuv420p "$ROOT/clips/04-home-checklist.mp4"

"$FFMPEG" -y -stream_loop -1 -i "$CURTAIN" -loop 1 -i "$ROOT/work/end.png" -t 13 \
  -filter_complex "[0:v]scale=-2:1920,crop=1080:1920,eq=brightness=-0.08:saturation=0.72,setsar=1[bg];[bg][1:v]overlay=0:0" -r 30 -pix_fmt yuv420p \
  "$ROOT/clips/05-curtain.mp4"

"$FFMPEG" -y -f concat -safe 0 -i "$ROOT/concat.txt" -i "$ROOT/work/narration.aiff" \
  -filter_complex "[1:a]apad=pad_dur=70[a]" -map 0:v -map "[a]" -t 70 \
  -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 160k "$ROOT/work/base.mp4"

"$FFMPEG" -y -i "$ROOT/work/base.mp4" \
  -c:v libx264 -preset medium -crf 20 -c:a copy -movflags +faststart \
  "$ROOT/renders/003-台风窗户贴胶带-初版.mp4"

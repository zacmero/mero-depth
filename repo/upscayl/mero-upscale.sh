#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  cat <<'EOF'
Usage:
  ./mero-upscale.sh INPUT OUTPUT [scale] [model]

Examples:
  ./mero-upscale.sh image.png image-4x.png
  ./mero-upscale.sh image.png image-2x.png 2 upscayl-lite-4x
  ./mero-upscale.sh ./input-folder ./output-folder 4 ultrasharp-4x

Models live in resources/models. Useful names:
  upscayl-standard-4x
  upscayl-lite-4x
  ultrasharp-4x
  ultramix-balanced-4x
  digital-art-4x
  high-fidelity-4x
  remacri-4x
EOF
  exit 2
fi

input=$1
output=$2
scale=${3:-4}
model=${4:-upscayl-standard-4x}

cd "$(dirname "$0")"
exec ./resources/linux/bin/upscayl-bin \
  -i "$input" \
  -o "$output" \
  -m resources/models \
  -n "$model" \
  -s "$scale" \
  -f png

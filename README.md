# DepthFlow local UI setup

This folder is a maintained local DepthFlow setup.

- Source lives in `repo/`.
- The Python environment lives in `.venv/` and is ignored by git.
- The venv is installed in editable mode from `repo/`.

## Reinstall after source changes

```bash
cd ~/projects/depthflow
uv pip install -e repo --python .venv/bin/python
```

Keep this in a venv, not global Python. It is easier to reproduce later on a VM and avoids global GPU/Python dependency mess.

## What DepthFlow does

```text
image -> DepthAnythingV2 depth estimate -> OpenGL DepthFlow shader -> live GLFW preview or FFmpeg MP4
```

DepthFlow turns one image plus a depth map into 3D parallax motion. If no depth map is provided, it estimates one with DepthAnythingV2.

## Live interactive UI

```bash
cd ~/projects/depthflow

.venv/bin/depthflow-ui \
  -i "/home/zacmero/Desktop/1_Projects/Relaxing Paradise/Automation Rendered/rp-source-1-depthflow-1080p.png"
```

Controls:

- `Animate`: toggle live motion.
- `Loops`: integer loop count. Use whole numbers so the end frame returns to the start frame.
- `Motion X` / `Motion Y`: parallax motion amount.
- `Quality`: preview/render shader quality.
- `Height`, `Steady`, `Focus`, `Zoom`, `Isometric`, `Dolly`: DepthFlow shader parameters.

The UI writes the current settings to this shell script every frame:

```bash
/tmp/depthflow-render-command.sh
```

After tuning the UI, render the exact current settings with:

```bash
bash /tmp/depthflow-render-command.sh
```

You can also click `Print render command` in the UI and copy it from the terminal.

## Render clean looped MP4

This renders without drawing the sliders into the video:

```bash
cd ~/projects/depthflow

.venv/bin/depthflow-ui \
  -i "/home/zacmero/Desktop/1_Projects/Relaxing Paradise/Automation Rendered/rp-source-1-depthflow-1080p.png" \
  -o "/home/zacmero/Desktop/1_Projects/Relaxing Paradise/Automation Rendered/depthflow-render.mp4" \
  -t 5 \
  -w 1920 \
  -h 1080 \
  --quality 80 \
  --height-effect 0.3 \
  --steady 0.15 \
  --focus 0 \
  --zoom 1 \
  --isometric 0.6 \
  --dolly 0 \
  --motion-x 0.4 \
  --motion-y 0.2 \
  --loops 1
```

Looping rule:

- `--loops 1` = one complete cycle over `-t` seconds.
- `--loops 2` = two complete cycles over `-t` seconds.
- Keep `--loops` as an integer. Integer loops close cleanly because the animation uses sine/cosine over DepthFlow's full scene cycle.

Notes:

- `-t` is video duration in seconds.
- `-w` / `-h` are output resolution.
- `--height-effect` is the parallax height/intensity.
- `-h` is output video height. Do not confuse it with `--height-effect`.
- `--quality` is the DepthFlow shader quality, not codec CRF.
- When `-o/--output` is used, the UI overlay is disabled automatically.

## Plain built-in command

The upstream command opens a basic scene but does not include our fader UI:

```bash
depthflow input IMAGE main
```

Use `depthflow-ui` instead.

## Common shell mistake

Line continuation must be a bare backslash at the end of a line:

```bash
# good
cmd \
  next-arg

# bad
cmd \ next-arg
```

## Git layout

Git is initialized at this root folder:

```bash
~/projects/depthflow
```

The nested `repo/.git` was removed so root git tracks the source files directly.

No commits are made by the agent. User commits manually.

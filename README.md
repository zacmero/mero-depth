# DepthFlow local UI setup

This folder is a maintained local DepthFlow setup.

- Source lives in `repo/`.
- The Python environment lives in `.venv/` and is ignored by git.
- The venv is installed in editable mode from `repo/`, so changes in `repo/` are used by commands immediately after reinstalling.

## Why venv, not global

Keep this in the venv. It is easier to reproduce on a VM and avoids global Python/GPU dependency mess.

Reinstall editable package after source changes:

```bash
cd ~/projects/depthflow
uv pip install -e repo --python .venv/bin/python
```

## What DepthFlow does

DepthFlow takes an input image, estimates or loads a depth map, then renders a 3D parallax effect through an OpenGL shader. For exported videos it pipes frames to FFmpeg.

Flow:

```text
image -> DepthAnythingV2 depth estimate -> OpenGL DepthFlow shader -> live GLFW window or FFmpeg MP4
```

## Live interactive UI

Use our added UI command:

```bash
cd ~/projects/depthflow

.venv/bin/depthflow-ui \
  -i "/home/zacmero/Desktop/1_Projects/Relaxing Paradise/Automation Rendered/rp-source-1-depthflow-1080p.png"
```

Controls:

- `Animate`: toggles live motion.
- `Speed`: animation speed.
- `Motion X` / `Motion Y`: parallax motion amount.
- `Height`, `Steady`, `Focus`, `Zoom`, `Isometric`, `Dolly`: DepthFlow shader parameters.

The plain built-in command below only opens a basic scene and does not include our fader UI:

```bash
depthflow input IMAGE main
```

## Render clean MP4

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
  --motion-x 0.4 \
  --motion-y 0.2 \
  --speed 1.0
```

Notes:

- `-t` is video duration in seconds.
- `-w` / `-h` are output resolution.
- `--quality` is the DepthFlow global render quality, not codec CRF.
- When `-o/--output` is used, the UI overlay is disabled automatically.

## Common shell mistake

Line continuation must be a bare backslash at the end of a line:

```bash
# good
cmd \
  next-arg

# bad: this escapes a space and breaks command parsing
cmd \ next-arg
```

The earlier `Unknown option: --height` happened because `state` was not parsed as a subcommand after a bad backslash.

## Git layout

Git is initialized at this root folder:

```bash
~/projects/depthflow
```

The nested `repo/.git` was removed so root git can track the source files directly.

Important changed files:

```text
repo/pyproject.toml
repo/depthflow/examples/__init__.py
repo/depthflow/examples/interactive.py
repo/.gitignore
README.md
.gitignore
```

No commits are made by the agent. User commits manually.

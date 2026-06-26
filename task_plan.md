# DepthFlow interactive UI + render fix plan

## Goal
Make DepthFlow usable with a local GUI: sliders should work, preview should animate, mouse hitbox should match cursor, and render command should output MP4 into the user's Automation Rendered folder.

## Phases
1. [complete] Record current issues and root causes
2. [complete] Patch interactive UI script
   - remove forced framebuffer scaling causing mouse offset
   - assign ImGui slider return values back to state
   - add animation controls that move the image live
   - add optional render args
3. [complete] Test UI launch and render command
4. [complete] Give exact commands and explain CLI backslash error
5. [complete] Organize project as tracked local fork
   - keep source changes in `repo/`
   - remove duplicate `repo_temp/` if clean
   - avoid editing `.venv` directly
   - initialize/keep git tracking in source repo
6. [complete] Patch render mode to hide UI overlay
7. [complete] Decide venv vs global install

## Errors Encountered
| Error | Cause | Fix |
|---|---|---|
| `depthflow --image` unknown command | image flag belongs to `input` subcommand | use `depthflow input ...` |
| sliders snap back | ImGui return values not assigned | patched script |
| mouse hitbox offset | forced `display_framebuffer_scale = 1.75` from docs video script | remove forced scale |
| `Unknown option: --height` in render | shell command used `\ state` on same line, escaping a space and preventing `state` as subcommand; also typo `--qualit` | use proper line continuations, no chars after `\`, correct `--quality` |
| no motion in GUI | static `DepthScene` state only; no animated update | add animate checkbox + speed/amplitude updating offset |

# Findings

- Local project root originally only had `.venv`; DepthFlow source was cloned to `repo/` and installed editable into `.venv` with `uv pip install -e repo --python .venv/bin/python`.
- Built-in `depthflow input ... main` opens a plain `DepthScene`; it does not draw the docs ImGui sliders.
- `examples/docs.py` has slider drawing code but is for headless documentation video generation. Its forced `imguio.display_framebuffer_scale = (1.75, 1.75)` is wrong for a live window and likely caused cursor hitbox mismatch.
- Current custom script: `repo/depthflow/examples/interactive.py` launches `ShaderFlow • InteractiveScene`.
- Render CLI order matters: commands are chained as `input IMAGE state [OPTIONS] main [OPTIONS]`. Shell line continuation must be a bare backslash at end of line, with no trailing characters.

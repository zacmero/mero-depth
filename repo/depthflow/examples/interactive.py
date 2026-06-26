import math
import shlex
from pathlib import Path
from typing import Annotated, Optional

from attrs import define
from cyclopts import App, Parameter
from imgui_bundle import imgui

from depthflow.scene import DepthScene

COMMAND_FILE = Path("/tmp/depthflow-render-command.sh")


@define
class RenderScene(DepthScene):
    motion_x: float = 0.0
    motion_y: float = -0.46
    loops: int = 1

    def update(self):
        t = self.cycle * self.loops
        self.state.offset = (self.motion_x * math.sin(t), self.motion_y * math.cos(t))


@define
class InteractiveScene(RenderScene):
    image_path: Path | None = None
    output_path: Path | None = None
    animate: bool = True
    show_ui: bool = True
    render_time: float = 5.0
    render_width: int = 1920
    render_height: int = 1080

    def render_command(self) -> str:
        output = self.output_path or (self.image_path.parent / "depthflow-render.mp4")
        args = [
            ".venv/bin/depthflow-ui",
            "-i", str(self.image_path),
            "-o", str(output),
            "-t", f"{self.render_time:g}",
            "-w", str(self.render_width),
            "-h", str(self.render_height),
            "--quality", f"{self.quality:g}",
            "--height-effect", f"{self.state.height:g}",
            "--steady", f"{self.state.steady:g}",
            "--focus", f"{self.state.focus:g}",
            "--zoom", f"{self.state.zoom:g}",
            "--isometric", f"{self.state.isometric:g}",
            "--dolly", f"{self.state.dolly:g}",
            "--motion-x", f"{self.motion_x:g}",
            "--motion-y", f"{self.motion_y:g}",
            "--loops", str(self.loops),
        ]
        if not self.state.sticky:
            args.append("--no-sticky")
        return "cd ~/projects/depthflow && \\\n  " + " \\\n  ".join(shlex.quote(x) for x in args) + "\n"

    def write_render_command(self):
        if self.image_path:
            COMMAND_FILE.write_text("#!/usr/bin/env bash\nset -e\n" + self.render_command())
            COMMAND_FILE.chmod(0o755)

    def _render_ui(self):
        imgui.push_style_var(imgui.StyleVar_.window_border_size, 0.0)
        imgui.push_style_var(imgui.StyleVar_.window_rounding, 8)
        imgui.push_style_var(imgui.StyleVar_.grab_rounding, 8)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 8)
        imgui.push_style_var(imgui.StyleVar_.child_rounding, 8)
        imgui.push_style_color(imgui.Col_.frame_bg, (0.1, 0.1, 0.1, 0.5))
        imgui.new_frame()
        imgui.set_next_window_pos((0, 0))
        imgui.set_next_window_bg_alpha(0.6)
        imgui.begin("Parameters", False, imgui.WindowFlags_.always_auto_resize)

        _, self.animate = imgui.checkbox("Animate", self.animate)
        _, loops = imgui.slider_int("Loops", self.loops, 1, 8)
        self.loops = loops
        _, self.motion_x = imgui.slider_float("Motion X", self.motion_x, -2, 2, "%.2f")
        _, self.motion_y = imgui.slider_float("Motion Y", self.motion_y, -2, 2, "%.2f")

        _, self.quality = imgui.slider_float("Quality", self.quality, 0, 100, "%.2f")
        _, self.state.height = imgui.slider_float("Height", self.state.height, 0, 1, "%.2f")
        _, self.state.steady = imgui.slider_float("Steady", self.state.steady, 0, 1, "%.2f")
        _, self.state.focus = imgui.slider_float("Focus", self.state.focus, 0, 1, "%.2f")
        _, self.state.zoom = imgui.slider_float("Zoom", self.state.zoom, 0, 2, "%.2f")
        _, self.state.isometric = imgui.slider_float("Isometric", self.state.isometric, 0, 1, "%.2f")
        _, self.state.dolly = imgui.slider_float("Dolly", self.state.dolly, 0, 5, "%.2f")
        _, self.state.sticky = imgui.checkbox("Sticky", self.state.sticky)

        if not self.animate:
            _, ox = imgui.slider_float("Offset X", self.state.offset[0], -2, 2, "%.2f")
            _, oy = imgui.slider_float("Offset Y", self.state.offset[1], -2, 2, "%.2f")
            self.state.offset = (ox, oy)

        _, rx = imgui.slider_float("Origin X", self.state.origin[0], -2, 2, "%.2f")
        _, ry = imgui.slider_float("Origin Y", self.state.origin[1], -2, 2, "%.2f")
        _, cx = imgui.slider_float("Center X", self.state.center[0], -2, 2, "%.2f")
        _, cy = imgui.slider_float("Center Y", self.state.center[1], -2, 2, "%.2f")
        self.state.origin = (rx, ry)
        self.state.center = (cx, cy)

        self.write_render_command()
        imgui.separator()
        imgui.text(f"Render script: {COMMAND_FILE}")
        if imgui.button("Print render command"):
            print("\n" + self.render_command(), flush=True)
        imgui.end()
        imgui.pop_style_color()
        imgui.pop_style_var(4)
        imgui.render()
        self._final.texture.fbo.use()
        self.imgui.render(imgui.get_draw_data())

    def update(self):
        if not getattr(self, "_ui_ready", False):
            self._ui_ready = True

        if self.show_ui:
            self._render_ui()
        if self.animate:
            RenderScene.update(self)


def run(
    image: Annotated[Path, Parameter(name=("--image", "-i"))],
    depth: Annotated[Optional[Path], Parameter(name=("--depth", "-d"))] = None,
    output: Annotated[Optional[Path], Parameter(name=("--output", "-o"))] = None,
    time: Annotated[float, Parameter(name=("--time", "-t"))] = 5.0,
    width: Annotated[int, Parameter(name=("--width", "-w"))] = 1920,
    height: Annotated[int, Parameter(name=("--height", "-h"))] = 1080,
    quality: Annotated[float, Parameter(name=("--quality", "-q"))] = 100.0,
    state_height: Annotated[float, Parameter(name="--height-effect")] = 0.19,
    steady: Annotated[float, Parameter(name="--steady")] = 0.15,
    focus: Annotated[float, Parameter(name="--focus")] = 0.0,
    zoom: Annotated[float, Parameter(name="--zoom")] = 1.0,
    isometric: Annotated[float, Parameter(name="--isometric")] = 0.58,
    dolly: Annotated[float, Parameter(name="--dolly")] = 1.51,
    sticky: Annotated[bool, Parameter(negative="--no-sticky")] = True,
    motion_x: Annotated[float, Parameter(name="--motion-x")] = 0.0,
    motion_y: Annotated[float, Parameter(name="--motion-y")] = -0.46,
    loops: Annotated[int, Parameter(name="--loops")] = 1,
):
    if output:
        scene = RenderScene(backend="headless", motion_x=motion_x, motion_y=motion_y, loops=loops)
    else:
        scene = InteractiveScene(
            image_path=image,
            output_path=output,
            motion_x=motion_x,
            motion_y=motion_y,
            loops=loops,
            render_time=time,
            render_width=width,
            render_height=height,
        )
    scene.quality = quality
    scene.state.height = state_height
    scene.state.steady = steady
    scene.state.focus = focus
    scene.state.zoom = zoom
    scene.state.isometric = isometric
    scene.state.dolly = dolly
    scene.state.sticky = sticky
    scene.input(image=image, depth=depth)
    if output:
        scene.main(output=output, time=time, width=width, height=height, quality=quality)
    else:
        scene.main(width=width, height=height, quality=quality)


def main():
    app = App(help_flags=[])
    app.default(run)
    app()


if __name__ == "__main__":
    main()

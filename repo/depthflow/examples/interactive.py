import math
from pathlib import Path
from typing import Annotated, Optional

from attrs import define
from cyclopts import App, Parameter
from imgui_bundle import imgui

from depthflow.scene import DepthScene


@define
class InteractiveScene(DepthScene):
    animate: bool = True
    show_ui: bool = True
    motion_x: float = 0.4
    motion_y: float = 0.0
    speed: float = 1.0

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
        _, self.speed = imgui.slider_float("Speed", self.speed, 0, 4, "%.2f")
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

        imgui.text("Render uses current CLI args, not live GUI tweaks yet.")
        imgui.end()
        imgui.pop_style_color()
        imgui.pop_style_var(4)
        imgui.render()
        self._final.texture.fbo.use()
        self.imgui.render(imgui.get_draw_data())

    def update(self):
        if not getattr(self, "_ui_ready", False):
            self.state.height = 0.3
            self.state.steady = 0.15
            self.state.focus = 0.0
            self.state.zoom = 1.0
            self.state.isometric = 0.6
            self.state.dolly = 0.0
            self.state.offset = (0.0, 0.0)
            self.state.center = (0.0, 0.0)
            self.state.origin = (0.0, 0.0)
            self._ui_ready = True

        if self.show_ui:
            self._render_ui()
        if self.animate:
            t = self.cycle * self.speed
            self.state.offset = (self.motion_x * math.sin(t), self.motion_y * math.cos(t))


def run(
    image: Annotated[Path, Parameter(name=("--image", "-i"))],
    depth: Annotated[Optional[Path], Parameter(name=("--depth", "-d"))] = None,
    output: Annotated[Optional[Path], Parameter(name=("--output", "-o"))] = None,
    time: Annotated[float, Parameter(name=("--time", "-t"))] = 5.0,
    width: Annotated[int, Parameter(name=("--width", "-w"))] = 1920,
    height: Annotated[int, Parameter(name=("--height", "-h"))] = 1080,
    quality: Annotated[float, Parameter(name=("--quality", "-q"))] = 80.0,
    motion_x: Annotated[float, Parameter(name="--motion-x")] = 0.4,
    motion_y: Annotated[float, Parameter(name="--motion-y")] = 0.0,
    speed: Annotated[float, Parameter(name="--speed")] = 1.0,
):
    scene = InteractiveScene(motion_x=motion_x, motion_y=motion_y, speed=speed)
    scene.input(image=image, depth=depth)
    if output:
        scene.show_ui = False
        scene.main(output=output, time=time, width=width, height=height, quality=quality)
    else:
        scene.main(width=width, height=height, quality=quality)


def main():
    app = App(help_flags=[])
    app.default(run)
    app()


if __name__ == "__main__":
    main()

from datetime import datetime

from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Container
from textual.widgets import Digits, Footer, Header, Tab, Tabs


class PomopodApp(App):
  CSS_PATH = "styles/base.tcss"

  BINDINGS: list[BindingType] = [
    Binding("space", "pause_resume", "Pause/Resume"),
    Binding("s", "start_stop", "Start/Stop"),
    Binding("r", "reset_time", "Reset Time"),
    Binding("c", "reset_count", "Reset Count"),
    Binding("q", "quit", "Quit"),
  ]

  def on_mount(self) -> None:
    self.theme = "catppuccin-mocha"

  def compose(self) -> ComposeResult:
    yield Header(id="header")
    with Container(id="content"):
      yield Tabs(
        Tab("Timer", id="timer"),
        Tab("Spaces", id="spaces"),
        Tab("Settings", id="settings"),
        id="tabs",
        active="timer",
      )
      yield Digits("00:00", id="timer")
    yield Footer(id="footer")

  def on_ready(self) -> None:
    self.update_clock()
    self.set_interval(1, self.update_clock)

  def update_clock(self) -> None:
    clock = datetime.now().time()
    self.query_one(Digits).update(f"{clock:%T}")


if __name__ == "__main__":
  PomopodApp().run()

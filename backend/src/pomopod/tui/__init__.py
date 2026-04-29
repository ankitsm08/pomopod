from rich import print as rprint

from pomopod.client import client
from pomopod.tui.app import PomopodApp


def app() -> None:
  """Launch pomopod TUI"""
  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return

  PomopodApp().run()

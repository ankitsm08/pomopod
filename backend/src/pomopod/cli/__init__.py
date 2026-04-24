import typer

from pomopod.cli.config import app as config
from pomopod.cli.daemon import app as daemon
from pomopod.cli.room import app as room
from pomopod.cli.space import app as space
from pomopod.cli.timer import app as timer

app = typer.Typer(help="Pomopod CLI")

app.add_typer(
  timer,
  name="timer",
  help="Manage pomodoro timer",
)
app.add_typer(
  daemon,
  name="daemon",
  help="Manage pomodoro daemon",
)
app.add_typer(
  space,
  name="space",
  help="Manage pomodoro spaces",
)
app.add_typer(
  config,
  name="config",
  help="Manage pomodoro config",
)
app.add_typer(
  room,
  name="room",
  help="Serve/Join pomodoro pods",
)

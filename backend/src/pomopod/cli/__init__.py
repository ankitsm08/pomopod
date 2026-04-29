from typer import Typer

from pomopod.cli.config import app as config
from pomopod.cli.daemon import app as daemon
from pomopod.cli.room import app as room
from pomopod.cli.space import app as space
from pomopod.cli.timer import app as timer
from pomopod.startup import startup_check

app = Typer(
  name="pomopod",
  help="Pomopod CLI",
  no_args_is_help=True,
)


@app.callback()
def startup():
  startup_check()


for typer in [timer, daemon, space, config, room]:
  app.add_typer(typer)


@app.command(name="tui", help="Launch pomopod TUI")
def tui():
  from pomopod.tui import app

  app()

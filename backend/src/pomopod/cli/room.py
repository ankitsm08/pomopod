from pathlib import Path
from typing import Optional

from typer import Typer, colors, echo, secho

app = Typer(
  name="room",
  help="Serve/Join pomodoro pods",
  no_args_is_help=True,
)


@app.command(name="serve")
def serve(host: str = "0.0.0.0", port: int = 8089, config: Optional[Path] = None):
  """Host a room"""
  if port < 0 or port > 65535:
    secho("Port must be between 0 and 65535", color=True, fg=colors.RED)
    return

  if host == "":
    echo("Host cannot be empty")
    return
  elif ("." in host and host.split(".") != 4) or (":" in host and host.split(":") != 6):
    echo("Invalid host")
    return

  if config:
    echo(f"Using custom config file at `{config}`")
  else:
    echo("Using default config file at `~/.config/pomopod/config.yaml`")

  echo("Starting server...")


@app.command(name="join")
def join(room_code: str):
  """Join a room"""
  echo(f"Joining room: {room_code}!")

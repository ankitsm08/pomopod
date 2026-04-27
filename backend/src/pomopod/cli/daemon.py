from typer import Option, Typer

from pomopod.core.constants import DEFAULT_DAEMON_HOST, DEFAULT_DAEMON_PORT

app = Typer(
  name="daemon",
  help="Manage pomodoro daemon",
  no_args_is_help=True,
)


def _spawn_daemon(host: str = DEFAULT_DAEMON_HOST, port: int = DEFAULT_DAEMON_PORT):
  """Spawn daemon in background using uvicorn."""
  import subprocess
  import sys

  from pomopod.server import state

  proc = subprocess.Popen(
    [
      sys.executable,
      "-m",
      "uvicorn",
      "pomopod.server.daemon:app",
      "--host",
      str(host),
      "--port",
      str(port),
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True,
  )

  state.save_daemon_pid(proc.pid)


@app.command(name="run")
def run_daemon():
  """Start the background daemon."""
  from rich import print as rprint

  from pomopod.client import client
  from pomopod.core import config

  if client.is_running():
    rprint("[yellow]Daemon already running[/yellow]")
    return

  daemon_config = config.get_daemon_settings()
  _spawn_daemon(daemon_config.host, daemon_config.port)
  rprint(
    "[green]Daemon started at [/green]"
    f"[cyan]http://{daemon_config.host}:{daemon_config.port}[/cyan]"
  )


@app.command(name="pid")
def show_daemon_pid():
  """Show the daemon PID."""
  import os

  from rich import print as rprint

  from pomopod.server import state

  pid = state.get_daemon_pid()
  if pid is None:
    rprint("[yellow]No daemon PID found[/yellow]")
    return

  # validate that the process is still running
  try:
    # does not kill, just checks if process exists
    os.kill(pid, 0)
    rprint(f"[green]Daemon PID: {pid}[/green]")
  except OSError:
    rprint(f"[red]Daemon PID {pid} found but process is not running[/red]")
    state.clear_daemon_pid()


@app.command(name="kill")
def kill_daemon(force: bool = Option(False, "--force", "-f", help="Force kill with SIGKILL")):
  """Kill the background daemon."""
  import os
  import signal

  from rich import print as rprint

  from pomopod.server import state

  pid = state.get_daemon_pid()
  if pid is None:
    rprint("[yellow]No daemon PID found[/yellow]")
    return

  try:
    if force:
      os.kill(pid, signal.SIGKILL)
      rprint(f"[red]Force killed daemon PID {pid}[/red]")
    else:
      os.kill(pid, signal.SIGTERM)
      rprint(f"[yellow]Sent termination signal to daemon PID {pid}[/yellow]")

    state.clear_daemon_pid()

  except OSError as e:
    rprint(f"[red]Failed to kill daemon PID {pid}: {e}[/red]")
    state.clear_daemon_pid()


@app.command(name="restart")
def restart_daemon(
  force: bool = Option(False, "--force", "-f", help="Force kill with SIGKILL"),
):
  """Restart the background daemon."""
  import os
  import time

  from rich import print as rprint

  from pomopod.server import state

  pid = state.get_daemon_pid()
  if pid is None:
    rprint("[yellow]No daemon PID found[/yellow]")
  else:
    kill_daemon(force)
    while True:
      try:
        os.kill(pid, 0)
        time.sleep(0.1)
      except OSError:
        break
  run_daemon()

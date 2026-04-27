from typer import Typer

from pomopod.err.client import handle_error

app = Typer(
  name="timer",
  help="Manage pomodoro timer",
  no_args_is_help=True,
)


@app.command(name="start")
def start_timer():
  """Start the pomodoro timer."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return

  try:
    client.start()
    rprint("[green]Timer started[/green]")
  except Exception as e:
    handle_error(e)


@app.command(name="pause")
def pause_timer():
  """Pause the timer."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running.[/red]")
    return

  try:
    client.pause()
    rprint("[yellow]Timer paused[/yellow]")
  except Exception as e:
    handle_error(e)


@app.command(name="resume")
def resume_timer():
  """Resume the timer."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running.[/red]")
    return

  try:
    client.resume()
    rprint("[green]Timer resumed[/green]")
  except Exception as e:
    handle_error(e)


@app.command(name="pause-resume")
def pause_resume_timer():
  """Toggle pause/resume the timer."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running.[/red]")
    return

  try:
    state = client.pause_resume()
    if state.is_paused:
      rprint("[yellow]Timer paused[/yellow]")
    else:
      rprint("[green]Timer resumed[/green]")
  except Exception as e:
    handle_error(e)


@app.command(name="stop")
def stop_timer():
  """Stop and reset the timer."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running.[/red]")
    return

  try:
    client.stop()
    rprint("[yellow]Timer stopped[/yellow]")
  except Exception as e:
    handle_error(e)


@app.command(name="status")
def show_status():
  """Show timer status."""
  from rich import print as rprint
  from rich.console import Console
  from rich.table import Table

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return

  try:
    status = client.get_status()
  except Exception as e:
    handle_error(e)
    return

  table = Table(title="Timer Status")
  table.add_column("Field", style="cyan")
  table.add_column("Value", style="green")

  table.add_row("Space", status.space_name)
  table.add_row("Type", status.current_type)
  table.add_row(
    "Session",
    f"{status.current_session_number}/{status.sessions_before_long_break}",
  )
  table.add_row("Paused", "Yes" if status.is_paused else "No")

  ms = status.remaining_time_ms
  minutes = ms // 60_000
  seconds = (ms % 60_000) // 1000
  table.add_row("Time Left", f"{minutes:02d}:{seconds:02d}")

  console = Console()
  console.print(table)


@app.command(name="reset-time")
def reset_time():
  """Reset the timer for current session."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running.[/red]")
    return

  try:
    client.reset_time()
    rprint("[yellow]Timer was reset successfully[/yellow]")
  except Exception as e:
    handle_error(e)


@app.command(name="reset-session-count")
def reset_session_count():
  """Reset the session count for current space."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running.[/red]")
    return

  try:
    client.reset_count()
    rprint("[yellow]Session count was reset successfully[/yellow]")
  except Exception as e:
    handle_error(e)

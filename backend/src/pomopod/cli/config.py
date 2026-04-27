from typing import Optional

from typer import Option, Typer

from pomopod.err.client import handle_error

app = Typer(
  name="config",
  help="Manage pomodoro config",
  no_args_is_help=True,
)


@app.command(name="init")
def init_configuration():
  """Initializes pomopod configuration with default values."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    result = client.init_config()
    rprint(f"[green]{result.get('message', 'Config initialized')}[/green]")
  except Exception as e:
    handle_error(e)


@app.command(name="show")
def show_configuration():
  """Show all pomopod configuration."""
  from rich import print as rprint
  from rich.console import Console
  from rich.table import Table

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    daemon_settings = client.get_daemon_settings()
    notification_settings = client.get_notification_settings()
    active_space_name = client.get_active_space_name()

    table = Table(title="PomoPod Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Active Space", active_space_name)
    table.add_row("Daemon Host", daemon_settings.host)
    table.add_row("Daemon Port", str(daemon_settings.port))
    table.add_row("Notifications", "Enabled" if notification_settings.enabled else "Disabled")

    console = Console()
    console.print(table)
  except Exception as e:
    handle_error(e)


@app.command(name="daemon")
def set_daemon_settings(
  host: Optional[str] = Option(
    None,
    "--host",
    "-h",
    help="Daemon host",
  ),
  port: Optional[int] = Option(
    None,
    "--port",
    "-p",
    help="Daemon port",
  ),
):
  """Set daemon settings."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    client.update_daemon_settings(host, port)
    rprint("[green]Daemon settings updated[/green]")
  except Exception as e:
    handle_error(e)


@app.command(name="notif")
def set_notification_settings(
  enable: Optional[bool] = Option(
    None,
    "--enable/--disable",
    "--yes/--no",
    help="Enable or disable notifications",
  ),
):
  """Toggle notification settings."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    if enable is None:
      setting = client.get_notification_settings()
      status = "[green]enabled[/green]" if setting.enabled else "[red]disabled[/red]"
      rprint(f"Notifications are {status}")
      return
    client.update_notification_settings(enable)
    if enable:
      rprint("Notifications are [green]enabled[/green]")
    else:
      rprint("Notifications are [red]disabled[/red]")
  except Exception as e:
    handle_error(e)

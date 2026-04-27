from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typer import Abort, Argument, Option, Typer, confirm, prompt

from pomopod.err.client import handle_error

if TYPE_CHECKING:
  from pomopod.core.models import Space

app = Typer(
  name="space",
  help="Manage pomodoro spaces",
  no_args_is_help=True,
)


def complete_spaces(incomplete: str) -> list[str]:
  from pomopod.client import client

  if not client.is_running():
    return []
  try:
    return [p for p in client.list_space_names() if p.startswith(incomplete)]
  except Exception:
    return []


@app.command(name="ls")
def list_spaces():
  """List all pomodoro spaces with details."""
  from rich import print as rprint
  from rich.console import Console
  from rich.table import Table

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    spaces = client.list_spaces()

    headers = ("Name", "Focus", "Short Break", "Long Break", "Sessions", "Color")
    table = Table(*headers, title="Spaces")

    for name, space in spaces.items():
      table.add_row(
        name,
        str(space.focus_duration),
        str(space.short_break_duration),
        str(space.long_break_duration),
        str(space.sessions_before_long_break),
        str(space.color),
      )

    console = Console()
    console.print(table)
  except Exception as e:
    handle_error(e)


def _print_space(space: Space):
  """Print the pomodoro space details."""
  from rich.console import Console
  from rich.table import Table

  table = Table(title=f"{space.name}")
  table.add_column("Setting", style="cyan")
  table.add_column("Value", style="green")

  table.add_row("Focus", str(space.focus_duration))
  table.add_row("Short Break", str(space.short_break_duration))
  table.add_row("Long Break", str(space.long_break_duration))
  table.add_row("Sessoins", str(space.sessions_before_long_break))
  table.add_row("Color", space.color)

  console = Console()
  console.print(table)


@app.command(name="show")
def show_active_space():
  """Show the active pomodoro space details."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    space = client.get_active_space()
    _print_space(space)
  except Exception as e:
    handle_error(e)


@app.command(name="set")
def set_space(
  name: str = Argument(
    ...,
    help="Name of the pomodoro space",
    autocompletion=complete_spaces,
  ),
):
  """Set the active pomodoro space."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    client.set_active_space(name)
    rprint(f'Active space set to [bold green]"{name}"[/bold green]')
  except Exception as e:
    handle_error(e)


def _validate_space(space_dict: dict) -> Space:
  from pydantic import ValidationError
  from rich import print as rprint

  from pomopod.core.models import Space

  try:
    return Space.model_validate(space_dict)
  except ValidationError as e:
    rprint("[bold red]\nInvalid space\n[/bold red]")
    rprint(f"Errors: {e.error_count()}")
    for error in e.errors():
      rprint(f"{error['loc']}: {error['msg']}")
    raise Abort()


@app.command(name="add")
def add_space(
  name: str = Argument(
    ...,
    help="Name of the new pomodoro space",
  ),
  focus: Optional[int] = Option(
    None,
    "--focus",
    help="Focus duration",
  ),
  short_break: Optional[int] = Option(
    None,
    "--short-break",
    help="Short break duration",
  ),
  long_break: Optional[int] = Option(
    None,
    "--long-break",
    help="Long break duration",
  ),
  sessions: Optional[int] = Option(
    None,
    "--sessions",
    help="Sessions before long break",
  ),
  color: Optional[str] = Option(
    None,
    "--color",
    help="Base color",
  ),
):
  """
  Add a new space.

  If options are provided, creates space non-interactively.
  Otherwise, prompts for each value.
  """
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    existing_names = client.list_space_names()
    if name in existing_names:
      rprint(f'Space [bold red]"{name}"[/bold red] already exists')
      return

    if any(v is not None for v in [focus, short_break, long_break, sessions, color]):
      space_dict = _add_space_non_interactive(name, focus, short_break, long_break, sessions, color)
    else:
      space_dict = _add_space_interactive(name)

    space = _validate_space(space_dict)
    client.add_space(space)
    rprint(f'Space [bold green]"{name}"[/bold green] added')
  except Exception as e:
    handle_error(e)


def _add_space_non_interactive(
  name: str,
  focus: Optional[int],
  short_break: Optional[int],
  long_break: Optional[int],
  sessions: Optional[int],
  color: Optional[str],
) -> dict:
  """Non-interactive space creation with defaults."""
  from pomopod.core.models import Space

  defaults = Space()

  return {
    "name": name,
    "focus_duration": (focus if focus is not None else defaults.focus_duration),
    "short_break_duration": (
      short_break if short_break is not None else defaults.short_break_duration
    ),
    "long_break_duration": (long_break if long_break is not None else defaults.long_break_duration),
    "sessions_before_long_break": (
      sessions if sessions is not None else defaults.sessions_before_long_break
    ),
    "color": (color if color is not None else defaults.color),
  }


def _add_space_interactive(name: str) -> dict:
  """Interactive space creation."""
  from rich import print as rprint

  rprint(f'Creating space [bold green]"{name}"[/bold green]:\n')
  rprint("Enter the durations in minutes.")
  focus = prompt("Focus duration", type=int)
  short_break = prompt("Short break duration", type=int)
  long_break = prompt("Long break duration", type=int)
  sessions = prompt("Sessions", type=int)
  color = prompt("Color", type=str)

  return {
    "name": name,
    "focus_duration": focus,
    "short_break_duration": short_break,
    "long_break_duration": long_break,
    "sessions_before_long_break": sessions,
    "color": color,
  }


@app.command(name="edit")
def edit_space(
  name: str = Argument(
    ...,
    help="Name of the pomodoro space",
    autocompletion=complete_spaces,
  ),
  new_name: str = Option(
    None,
    "--new-name",
    help="New name of the space",
  ),
  focus: Optional[int] = Option(
    None,
    "--focus",
    help="Focus duration",
  ),
  short_break: Optional[int] = Option(
    None,
    "--short-break",
    help="Short break duration",
  ),
  long_break: Optional[int] = Option(
    None,
    "--long-break",
    help="Long break duration",
  ),
  sessions: Optional[int] = Option(
    None,
    "--sessions",
    help="Sessions before long break",
  ),
  color: Optional[str] = Option(
    None,
    "--color",
    help="Base color",
  ),
):
  """
  Edit an existing profile.

  If options are provided, updates only those values.
  Otherwise, shows current values and prompts for new ones.
  """
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    existing_names = client.list_space_names()
    if name not in existing_names:
      rprint(f'Space [bold red]"{name}"[/bold red] does not exist')
      return
    if new_name and new_name in existing_names:
      rprint(f'Space [bold red]"{new_name}"[/bold red] already exists')
      return

    space = client.get_space(name)

    if any(v is not None for v in [new_name, focus, short_break, long_break, sessions, color]):
      space_dict = _edit_space_non_interactive(
        space, new_name, focus, short_break, long_break, sessions, color
      )
    else:
      space_dict = _edit_space_interactive(space)

    updated_space = _validate_space(space_dict)
    client.edit_space(name, updated_space)
    rprint(f'Space [bold green]"{name}"[/bold green] edited')
  except Exception as e:
    handle_error(e)


def _edit_space_non_interactive(
  space: Space,
  name: Optional[str],
  focus: Optional[int],
  short_break: Optional[int],
  long_break: Optional[int],
  sessions: Optional[int],
  color: Optional[str],
) -> dict:
  """Non-interactive space creation with defaults."""

  return {
    "name": (name if name is not None else space.name),
    "focus_duration": (focus if focus is not None else space.focus_duration),
    "short_break_duration": (
      short_break if short_break is not None else space.short_break_duration
    ),
    "long_break_duration": (long_break if long_break is not None else space.long_break_duration),
    "sessions_before_long_break": (
      sessions if sessions is not None else space.sessions_before_long_break
    ),
    "color": (color if color is not None else space.color),
  }


def _edit_space_interactive(space: Space) -> dict:
  """Interactive space editing."""
  from rich import print as rprint

  _print_space(space)

  rprint("\nEnter the durations in minutes. Leave empty to keep the current value.")
  name = prompt("Name", default=space.name, type=str)
  focus = prompt("Focus duration", default=space.focus_duration, type=int)
  short_break = prompt("Short break duration", default=space.short_break_duration, type=int)
  long_break = prompt("Long break duration", default=space.long_break_duration, type=int)
  sessions = prompt("Sessions", default=space.sessions_before_long_break, type=int)
  color = prompt("Color", default=space.color, type=str)

  return {
    "name": name,
    "focus_duration": focus,
    "short_break_duration": short_break,
    "long_break_duration": long_break,
    "sessions_before_long_break": sessions,
    "color": color,
  }


@app.command(name="rm")
def remove_space(
  name: str = Argument(
    ...,
    help="Name of the space to remove",
    autocompletion=complete_spaces,
  ),
  force: bool = Option(
    False,
    "--force",
    "-f",
    help="Delete without confirmation",
  ),
):
  """Remove a pomodoro space."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    existing_names = client.list_space_names()
    if name not in existing_names:
      rprint(f'Space [bold red]"{name}"[/bold red] does not exist')
      return

    active_space_name = client.get_active_space_name()
    if name == active_space_name:
      rprint(f'Cannot delete active space [bold red]"{name}"[/bold red]')
      return

    if not force:
      confirm(f'Delete the "{name}" space?', abort=True)

    client.remove_space(name)
    rprint(f'Space [bold green]"{name}"[/bold green] removed permanently')
  except Exception as e:
    handle_error(e)


@app.command(name="rename")
def rename_space(
  name: str = Argument(
    ...,
    help="Name of the space to rename",
    autocompletion=complete_spaces,
  ),
  new_name: Optional[str] = Option(
    None,
    "--new-name",
    "-n",
    help="New name of the space",
  ),
):
  """Rename a pomodoro space."""
  from rich import print as rprint

  from pomopod.client import client

  if not client.is_running():
    rprint("[red]Daemon not running. Run 'pomopod daemon run' first.[/red]")
    return
  try:
    existing_names = client.list_space_names()
    if name not in existing_names:
      rprint(f'Space [bold red]"{name}"[/bold red] does not exist')
      return

    if not new_name:
      new_name_input = prompt(f'New name for "{name}" space')
      new_name = str(new_name_input)

    if new_name in existing_names:
      rprint(f'Space [bold red]"{new_name}"[/bold red] already exists')
      return

    active_space_name = client.get_active_space_name()
    rename_active = name == active_space_name

    client.rename_space(name, new_name)
    rprint(
      f'Space [bold green]"{name}"[/bold green] renamed to [bold green]"{new_name}"[/bold green]'
    )

    if rename_active:
      set_space(new_name)
  except Exception as e:
    handle_error(e)

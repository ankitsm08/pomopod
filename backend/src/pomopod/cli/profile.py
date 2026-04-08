from typing import Optional

import typer
from pydantic import ValidationError
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from pomopod.core import config

app = typer.Typer()
console = Console()


@app.command()
def list():
  conf = config.load_config()

  headers = ("Name", "Focus", "Short Break", "Long Break", "Sessions", "Color")
  table = Table(*headers, title="Profiles")

  for name, prof in conf.profiles.items():
    table.add_row(
      name,
      str(prof.focus_duration),
      str(prof.short_break_duration),
      str(prof.long_break_duration),
      str(prof.sessions_until_long_break),
      str(prof.color),
    )

  console.print(table)


@app.command()
def set(name: str = typer.Argument(...)):
  prof = config.set_active_profile(name)
  if not prof:
    rprint(f'Profile [bold red]"{name}"[/bold red] does not exist')
  else:
    rprint(f'Active profile set to [bold green]"{name}"[/bold green]')


@app.command()
def add(name: str = typer.Argument(...)):
  if name in config.get_profile_names():
    rprint(f'Profile [bold red]"{name}"[/bold red] already exists')
    return

  rprint("Enter the durations in minutes.")
  focus_duration = int(typer.prompt("Focus duration"))
  short_break_duration = int(typer.prompt("Short break duration"))
  long_break_duration = int(typer.prompt("Long break duration"))
  sessions_before_long_break = int(typer.prompt("Sessions"))
  color = str(typer.prompt("Color"))

  try:
    prof = config.Profile.model_validate(
      config.Profile(
        focus_duration=focus_duration,
        short_break_duration=short_break_duration,
        long_break_duration=long_break_duration,
        sessions_until_long_break=sessions_before_long_break,
        color=color,
      )
    )
  except ValidationError as e:
    rprint("[bold red]\nInvalid profile\n[/bold red]")
    rprint(f"Errors: {e.error_count()}")
    for error in e.errors():
      rprint(f"{error['loc']}: {error['msg']}")
    return

  prof = config.add_profile(name, prof)

  if not prof:
    rprint(f'Profile [bold red]"{name}"[/bold red] already exists')
  else:
    rprint(f'Profile [bold green]"{name}"[/bold green] added')


@app.command()
def remove(name: str = typer.Argument(...), force: bool = typer.Option(False, "--force", "-f")):
  if name not in config.get_profile_names():
    rprint(f'Profile [bold red]"{name}"[/bold red] does not exist')
    return

  if name == config.get_active_profile_name():
    rprint(f'Cannot delete active profile [bold red]"{name}"[/bold red]')
    return

  if not force:
    typer.confirm(f'Delete the "{name}" profile?', abort=True)

  prof = config.remove_profile(name)

  if not prof:
    rprint(f'Profile [bold red]"{name}"[/bold red] does not exist')
  else:
    rprint(f'Profile [bold green]"{name}"[/bold green] removed permanantly')


@app.command()
def rename(name: str = typer.Argument(...), new_name: Optional[str] = None):
  if name not in config.get_profile_names():
    rprint(f'Profile [bold red]"{name}"[/bold red] does not exist')
    return

  if not new_name:
    new_name_input = typer.prompt(f'New name for "{name}" profile')
    new_name = str(new_name_input)

  if new_name in config.get_profile_names():
    rprint(f'Profile [bold red]"{name}"[/bold red] already exists')
    return

  rename_active_profile = name == config.get_active_profile_name()

  prof = config.remove_profile(name)

  if not prof:
    rprint(f'Profile [bold red]"{name}"[/bold red] does not exist')
    return

  prof = config.add_profile(new_name, prof)

  if not prof:
    rprint(f'Profile [bold red]"{name}"[/bold red] already exists')
  else:
    rprint(
      f'Profile [bold green]"{name}"[/bold green] renamed to [bold green]"{new_name}"[/bold green]'
    )

  if rename_active_profile:
    set(new_name)

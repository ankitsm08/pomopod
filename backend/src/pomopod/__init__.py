from rich import print as rprint

from pomopod.core import config, state
from pomopod.core.constants import DEFAULT_ACTIVE_SPACE

if not config.is_config_correct():
  rprint(
    "[bold red]Config file is not correct.[/bold red]\n"
    "Please run 'pomopod config init' or fix the config file manually"
  )

if not state._is_active_space_set():
  spaces = config.get_space_names()
  if len(spaces) > 0:
    state.set_active_space(spaces[0])
  else:
    conf = config._load_config()
    conf.spaces = config._get_default_config().spaces
    config._save_config(conf)
    state.set_active_space(DEFAULT_ACTIVE_SPACE)
    rprint(
      "[bold red]No active space was set and no spaces were found.[/bold red]\n"
      "Setting the active space to default (work) and resetting the config file"
    )

import json
from pathlib import Path

from pydantic import ValidationError

from pomopod.core.models import Config, Profile

CONFIG_DIR = Path.home() / ".config" / "pomopod"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir() -> None:
  CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_default_config() -> Config:
  return Config()


def load_config() -> Config:
  if not CONFIG_FILE.exists():
    config = get_default_config()
    save_config(config)
    return config

  with open(CONFIG_FILE, "r") as f:
    config_json = json.load(f)

  try:
    config = Config.model_validate(config_json)
  except ValidationError:
    return get_default_config()

  return config


def save_config(config: Config) -> None:
  ensure_config_dir()
  with open(CONFIG_FILE, "w") as f:
    json.dump(config.model_dump(), f, indent=2)


def get_profiles() -> dict[str, Profile]:
  config = load_config()
  return config.profiles


def get_profile_names() -> list[str]:
  config = load_config()
  return list(config.profiles.keys())


def get_active_profile_name() -> str:
  config = load_config()
  return config.active_profile


def get_active_profile() -> Profile | None:
  config = load_config()
  return config.profiles.get(config.active_profile)


def set_active_profile(name: str) -> Profile | None:
  config = load_config()

  if name in config.profiles.keys():
    config.active_profile = name
    save_config(config)

  return config.profiles.get(name)


def add_profile(name: str, profile: Profile) -> Profile | None:
  config = load_config()

  if name in list(config.profiles.keys()):
    return None

  config.profiles[name] = profile
  save_config(config)
  return profile


def remove_profile(name: str) -> Profile | None:
  config = load_config()

  if name not in list(config.profiles.keys()):
    return None

  profile = config.profiles.pop(name)
  save_config(config)
  return profile

from abc import ABC, abstractmethod
from typing import Any, Optional

from pomopod.core.models import (
  DaemonSettings,
  Health,
  NotificationSettings,
  Space,
  TimerState,
)


class PomopodClient(ABC):
  @abstractmethod
  def is_running(self) -> bool | Any: ...

  # Timer endpoints
  @abstractmethod
  def get_health(self) -> Health | Any: ...

  @abstractmethod
  def get_status(self) -> TimerState | Any: ...

  @abstractmethod
  def start(self) -> TimerState | Any: ...

  @abstractmethod
  def pause(self) -> TimerState | Any: ...

  @abstractmethod
  def resume(self) -> TimerState | Any: ...

  @abstractmethod
  def pause_resume(self) -> TimerState | Any: ...

  @abstractmethod
  def stop(self) -> TimerState | Any: ...

  @abstractmethod
  def reset_time(self) -> TimerState | Any: ...

  @abstractmethod
  def reset_count(self) -> TimerState | Any: ...

  # Space endpoints
  @abstractmethod
  def get_active_space(self) -> Space | Any: ...

  @abstractmethod
  def get_active_space_name(self) -> str | Any: ...

  @abstractmethod
  def set_active_space(self, space_name: str) -> Space | Any: ...

  @abstractmethod
  def list_spaces(self) -> dict[str, Space] | Any: ...

  @abstractmethod
  def list_space_names(self) -> list[str] | Any: ...

  @abstractmethod
  def get_space(self, space_name: str) -> Space | Any: ...

  @abstractmethod
  def add_space(self, space: Space) -> Space | Any: ...

  @abstractmethod
  def edit_space(self, space_name: str, space: Space) -> Space | Any: ...

  @abstractmethod
  def remove_space(self, space_name: str) -> Space | Any: ...

  @abstractmethod
  def rename_space(self, space_name: str, new_name: str) -> Space | Any: ...

  # Config endpoints
  @abstractmethod
  def init_config(self) -> dict | Any: ...

  @abstractmethod
  def get_daemon_settings(self) -> DaemonSettings | Any: ...

  @abstractmethod
  def get_notification_settings(self) -> NotificationSettings | Any: ...

  @abstractmethod
  def update_daemon_settings(
    self, host: Optional[str] = None, port: Optional[int] = None
  ) -> DaemonSettings | Any: ...

  @abstractmethod
  def update_notification_settings(self, enable: bool) -> NotificationSettings | Any: ...

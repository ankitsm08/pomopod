from abc import ABC, abstractmethod
from typing import Optional

from pomopod.core.models import (
  DaemonSettings,
  Health,
  NotificationSettings,
  Space,
  TimerState,
)


class PomopodClient(ABC):
  @abstractmethod
  def is_running(self) -> bool: ...

  # Timer endpoints
  @abstractmethod
  def get_health(self) -> Health: ...

  @abstractmethod
  def get_status(self) -> TimerState: ...

  @abstractmethod
  def start(self) -> TimerState: ...

  @abstractmethod
  def pause(self) -> TimerState: ...

  @abstractmethod
  def resume(self) -> TimerState: ...

  @abstractmethod
  def pause_resume(self) -> TimerState: ...

  @abstractmethod
  def stop(self) -> TimerState: ...

  @abstractmethod
  def reset_time(self) -> TimerState: ...

  @abstractmethod
  def reset_count(self) -> TimerState: ...

  # Space endpoints
  @abstractmethod
  def get_active_space(self) -> Space: ...

  @abstractmethod
  def get_active_space_name(self) -> str: ...

  @abstractmethod
  def set_active_space(self, space_name: str) -> Space: ...

  @abstractmethod
  def list_spaces(self) -> dict[str, Space]: ...

  @abstractmethod
  def list_space_names(self) -> list[str]: ...

  @abstractmethod
  def get_space(self, space_name: str) -> Space: ...

  @abstractmethod
  def add_space(self, space: Space) -> Space: ...

  @abstractmethod
  def edit_space(self, space_name: str, space: Space) -> Space: ...

  @abstractmethod
  def remove_space(self, space_name: str) -> Space: ...

  @abstractmethod
  def rename_space(self, space_name: str, new_name: str) -> Space: ...

  # Config endpoints
  @abstractmethod
  def init_config(self) -> dict: ...

  @abstractmethod
  def get_daemon_settings(self) -> DaemonSettings: ...

  @abstractmethod
  def get_notification_settings(self) -> NotificationSettings: ...

  @abstractmethod
  def update_daemon_settings(
    self, host: Optional[str] = None, port: Optional[int] = None
  ) -> DaemonSettings: ...

  @abstractmethod
  def update_notification_settings(self, enable: bool) -> NotificationSettings: ...

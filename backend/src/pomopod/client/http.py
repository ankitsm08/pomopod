from typing import Optional

import httpx

from pomopod.client.base import PomopodClient
from pomopod.core.models import (
  DaemonSettings,
  Health,
  NotificationSettings,
  Space,
  TimerState,
)
from pomopod.err.client import PomopodClientError


class HttpPomopodClient(PomopodClient):
  def __init__(self, base_url: str):
    self.client = httpx.Client(base_url=base_url, timeout=5)

  def _handle_response(self, r: httpx.Response, model_class):
    if r.status_code >= 400:
      raise PomopodClientError(r.status_code, r.text)
    data = r.json()

    # pydantic models
    if hasattr(model_class, "model_validate"):
      return model_class.model_validate(data)

    # generic types
    return data

  def is_running(self) -> bool:
    try:
      r = self.client.get("/")
      return r.status_code == 200
    except httpx.HTTPError:
      return False

  # Timer endpoints
  def get_health(self) -> Health:
    r = self.client.get("/")
    return self._handle_response(r, Health)

  def get_status(self) -> TimerState:
    r = self.client.get("/status")
    return self._handle_response(r, TimerState)

  def start(self) -> TimerState:
    r = self.client.post("/start")
    return self._handle_response(r, TimerState)

  def pause(self) -> TimerState:
    r = self.client.post("/pause")
    return self._handle_response(r, TimerState)

  def resume(self) -> TimerState:
    r = self.client.post("/resume")
    return self._handle_response(r, TimerState)

  def pause_resume(self) -> TimerState:
    r = self.client.post("/pause-resume")
    return self._handle_response(r, TimerState)

  def stop(self) -> TimerState:
    r = self.client.post("/stop")
    return self._handle_response(r, TimerState)

  def reset_time(self) -> TimerState:
    r = self.client.post("/reset-time")
    return self._handle_response(r, TimerState)

  def reset_count(self) -> TimerState:
    r = self.client.post("/reset-count")
    return self._handle_response(r, TimerState)

  # Space endpoints
  def get_active_space(self) -> Space:
    r = self.client.get("/spaces/active")
    return self._handle_response(r, Space)

  def get_active_space_name(self) -> str:
    r = self.client.get("/spaces/active/name")
    return self._handle_response(r, str)

  def set_active_space(self, space_name: str) -> Space:
    r = self.client.post(f"/spaces/active/{space_name}")
    return self._handle_response(r, Space)

  def list_spaces(self) -> dict[str, Space]:
    r = self.client.get("/spaces/list")
    if r.status_code >= 400:
      raise PomopodClientError(r.status_code, r.text)
    data = r.json()
    return {k: Space.model_validate(v) for k, v in data.items()}

  def list_space_names(self) -> list[str]:
    r = self.client.get("/spaces/list-names")
    return self._handle_response(r, list[str])

  def get_space(self, space_name: str) -> Space:
    r = self.client.get(f"/spaces/{space_name}")
    return self._handle_response(r, Space)

  def add_space(self, space: Space) -> Space:
    r = self.client.post("/spaces", json=space.model_dump())
    return self._handle_response(r, Space)

  def edit_space(self, space_name: str, space: Space) -> Space:
    r = self.client.patch(f"/spaces/{space_name}", json=space.model_dump())
    return self._handle_response(r, Space)

  def remove_space(self, space_name: str) -> Space:
    r = self.client.delete(f"/spaces/{space_name}")
    return self._handle_response(r, Space)

  def rename_space(self, space_name: str, new_name: str) -> Space:
    r = self.client.patch(f"/spaces/rename/{space_name}", params={"new_name": new_name})
    return self._handle_response(r, Space)

  # Config endpoints
  def init_config(self) -> dict:
    r = self.client.post("/config/init")
    return self._handle_response(r, dict)

  def get_daemon_settings(self) -> DaemonSettings:
    r = self.client.get("/config/daemon")
    return self._handle_response(r, DaemonSettings)

  def get_notification_settings(self) -> NotificationSettings:
    r = self.client.get("/config/notif")
    return self._handle_response(r, NotificationSettings)

  def update_daemon_settings(
    self, host: Optional[str] = None, port: Optional[int] = None
  ) -> DaemonSettings:
    params = {}
    if host is not None:
      params["host"] = host
    if port is not None:
      params["port"] = port
    r = self.client.post("/config/daemon", params=params)
    return self._handle_response(r, DaemonSettings)

  def update_notification_settings(self, enable: bool) -> NotificationSettings:
    r = self.client.post("/config/notif", params={"enable": enable})
    return self._handle_response(r, NotificationSettings)

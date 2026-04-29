from typing import Any, Optional

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


class AsyncHttpPomopodClient(PomopodClient):
  def __init__(self, base_url: str):
    self.client = httpx.AsyncClient(base_url=base_url, timeout=5)

  async def close(self):
    await self.client.aclose()

  async def __aenter__(self):
    return self

  async def __aexit__(self, _exc_type, _exc, _tb):
    await self.close()

  def _handle_response(self, r: httpx.Response, model_class) -> Any:
    if r.status_code >= 400:
      raise PomopodClientError(r.status_code, r.text)

    data = r.json()

    # pydantic models
    if hasattr(model_class, "model_validate"):
      return model_class.model_validate(data)

    # generic types
    return data

  async def is_running(self) -> bool:
    try:
      r = await self.client.get("/")
      return r.status_code == 200
    except httpx.HTTPError:
      return False

  # Timer endpoints
  async def get_health(self) -> Health:
    r = await self.client.get("/")
    return self._handle_response(r, Health)

  async def get_status(self) -> TimerState:
    r = await self.client.get("/status")
    return self._handle_response(r, TimerState)

  async def start(self) -> TimerState:
    r = await self.client.post("/start")
    return self._handle_response(r, TimerState)

  async def pause(self) -> TimerState:
    r = await self.client.post("/pause")
    return self._handle_response(r, TimerState)

  async def resume(self) -> TimerState:
    r = await self.client.post("/resume")
    return self._handle_response(r, TimerState)

  async def pause_resume(self) -> TimerState:
    r = await self.client.post("/pause-resume")
    return self._handle_response(r, TimerState)

  async def stop(self) -> TimerState:
    r = await self.client.post("/stop")
    return self._handle_response(r, TimerState)

  async def reset_time(self) -> TimerState:
    r = await self.client.post("/reset-time")
    return self._handle_response(r, TimerState)

  async def reset_count(self) -> TimerState:
    r = await self.client.post("/reset-count")
    return self._handle_response(r, TimerState)

  # Space endpoints
  async def get_active_space(self) -> Space:
    r = await self.client.get("/spaces/active")
    return self._handle_response(r, Space)

  async def get_active_space_name(self) -> str:
    r = await self.client.get("/spaces/active/name")
    return self._handle_response(r, str)

  async def set_active_space(self, space_name: str) -> Space:
    r = await self.client.post(f"/spaces/active/{space_name}")
    return self._handle_response(r, Space)

  async def list_spaces(self) -> dict[str, Space]:
    r = await self.client.get("/spaces/list")
    if r.status_code >= 400:
      raise PomopodClientError(r.status_code, r.text)

    data = r.json()
    return {k: Space.model_validate(v) for k, v in data.items()}

  async def list_space_names(self) -> list[str]:
    r = await self.client.get("/spaces/list-names")
    return self._handle_response(r, list[str])

  async def get_space(self, space_name: str) -> Space:
    r = await self.client.get(f"/spaces/{space_name}")
    return self._handle_response(r, Space)

  async def add_space(self, space: Space) -> Space:
    r = await self.client.post("/spaces", json=space.model_dump())
    return self._handle_response(r, Space)

  async def edit_space(self, space_name: str, space: Space) -> Space:
    r = await self.client.patch(f"/spaces/{space_name}", json=space.model_dump())
    return self._handle_response(r, Space)

  async def remove_space(self, space_name: str) -> Space:
    r = await self.client.delete(f"/spaces/{space_name}")
    return self._handle_response(r, Space)

  async def rename_space(self, space_name: str, new_name: str) -> Space:
    r = await self.client.patch(f"/spaces/rename/{space_name}", params={"new_name": new_name})
    return self._handle_response(r, Space)

  # Config endpoints
  async def init_config(self) -> dict:
    r = await self.client.post("/config/init")
    return self._handle_response(r, dict)

  async def get_daemon_settings(self) -> DaemonSettings:
    r = await self.client.get("/config/daemon")
    return self._handle_response(r, DaemonSettings)

  async def get_notification_settings(self) -> NotificationSettings:
    r = await self.client.get("/config/notif")
    return self._handle_response(r, NotificationSettings)

  async def update_daemon_settings(
    self, host: Optional[str] = None, port: Optional[int] = None
  ) -> DaemonSettings:
    params = {}
    if host is not None:
      params["host"] = host
    if port is not None:
      params["port"] = port

    r = await self.client.post("/config/daemon", params=params)
    return self._handle_response(r, DaemonSettings)

  async def update_notification_settings(self, enable: bool) -> NotificationSettings:
    r = await self.client.post("/config/notif", params={"enable": enable})
    return self._handle_response(r, NotificationSettings)

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from pomopod.client.asynchttp import AsyncHttpPomopodClient
  from pomopod.client.http import HttpPomopodClient


_client_sync = None
_client_async = None


def get_client_sync(new: bool = False) -> HttpPomopodClient:
  global _client_sync
  if _client_sync is not None and not new:
    return _client_sync

  from pomopod.client.http import HttpPomopodClient

  _client_sync = HttpPomopodClient(base_url=daemon_url())
  return _client_sync


def get_client_async(new: bool = False) -> AsyncHttpPomopodClient:
  global _client_async
  if _client_async is not None and not new:
    return _client_async

  from pomopod.client.asynchttp import AsyncHttpPomopodClient

  _client_async = AsyncHttpPomopodClient(base_url=daemon_url())
  return _client_async


def daemon_url():
  from pomopod.core import config as core_config

  daemon_config = core_config.get_daemon_settings()
  return f"http://{daemon_config.host}:{daemon_config.port}"

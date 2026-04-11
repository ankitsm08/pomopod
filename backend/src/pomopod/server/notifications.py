try:
  from plyer import notification
except ImportError:
  notification: None = None


def _notify(title: str, message: str):
  """Send desktop notification. Fails silently if plyer not available."""
  if notification is None:
    return

  try:
    notification.notify(
      title=title,
      message=message,
      app_name="PomoPod",
      # TODO: Add icon (ico for windows)
      # read https://plyer.readthedocs.io/en/latest/api.html#plyer.facades.Notification
      # app_icon="path/to/icon.png",
      timeout=10,
    )
  except Exception:
    pass


def notify_session_start(session_type: str) -> None:
  _notify(
    title="Pomopod Started",
    message=f"{session_type} session started.",
  )


def notify_session_stop() -> None:
  _notify(
    title="Pomopod Stopped",
    message="Pomopod has stopped.",
  )


def notify_session_pause(session_type: str) -> None:
  _notify(
    title="Pomopod Paused",
    message=f"{session_type} session paused.",
  )


def notify_session_resume(session_type: str) -> None:
  _notify(
    title="Pomopod Resumed",
    message=f"{session_type} session resumed.",
  )

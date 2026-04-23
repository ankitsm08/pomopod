import json

from pydantic import ValidationError

from pomopod.core.models import TimerState
from pomopod.core.state import STATE_DIR, _ensure_state_dir

TIMER_STATE_FILE = STATE_DIR / "timer_state.json"
DAEMON_PID_FILE = STATE_DIR / "daemon.pid"


def save_timer_state(timer_state: TimerState) -> None:
  """Save the timer state to file."""
  _ensure_state_dir()

  data = timer_state.model_dump()
  with TIMER_STATE_FILE.open("w") as f:
    json.dump(data, f, indent=2)


def load_timer_state() -> TimerState | None:
  """Load the timer state from file."""
  _ensure_state_dir()
  if not TIMER_STATE_FILE.exists():
    return None

  try:
    with TIMER_STATE_FILE.open("r") as f:
      data_dict = json.load(f)
    return TimerState.model_validate(data_dict)
  except json.JSONDecodeError, ValidationError:
    clear_timer_state()
    return None


def clear_timer_state() -> None:
  """Clear the timer state file."""
  _ensure_state_dir()
  if TIMER_STATE_FILE.exists():
    TIMER_STATE_FILE.unlink(missing_ok=True)


def save_daemon_pid(pid: int) -> None:
  """Save the daemon PID to file."""
  _ensure_state_dir()
  with DAEMON_PID_FILE.open("w") as f:
    f.write(str(pid))


def get_daemon_pid() -> int | None:
  """Get the daemon PID from file."""
  _ensure_state_dir()
  if not DAEMON_PID_FILE.exists():
    return None

  try:
    pid_str = DAEMON_PID_FILE.read_text().strip()
    return int(pid_str) if pid_str else None
  except ValueError, OSError:
    return None


def clear_daemon_pid() -> None:
  """Clear the daemon PID file."""
  _ensure_state_dir()
  if DAEMON_PID_FILE.exists():
    DAEMON_PID_FILE.unlink(missing_ok=True)

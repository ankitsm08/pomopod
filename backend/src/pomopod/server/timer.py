import threading
from typing import Callable, Optional

from pomopod.core.models import Space, TimerState


class TimerManager:
  def __init__(self):
    self._timer = None
    self._stop_event = threading.Event()
    self._callback: Optional[Callable[[Space], None]] = None
    self._space: Optional[Space] = None
    self._timer_state: Optional[TimerState] = None
    self._lock = threading.Lock()

  def change_space(self, space: Space) -> None:
    """Change space and restart timer."""
    with self._lock:
      callback = self._callback
      timer_state = self._timer_state

    if callback and timer_state:
      self.start(callback, space, timer_state)

  def start(self, callback: Callable[[Space], None], space: Space, timer_state: TimerState):
    """Start a fresh background timer with a callback function."""
    self.stop()

    with self._lock:
      self._callback = callback
      self._space = space
      self._timer_state = timer_state
      self._stop_event.clear()

      self._timer = threading.Thread(target=self._run_loop, daemon=True)
      self._timer.start()

  def stop(self):
    """Stop the current timer thread."""
    self._stop_event.set()
    if self._timer and self._timer.is_alive():
      self._timer.join(timeout=2)
    self._timer = None

  def _run_loop(self):
    """Main loop that runs in background thread."""
    while not self._stop_event.is_set():
      with self._lock:
        # get current state
        callback = self._callback
        space = self._space
        timer_state = self._timer_state

      if not callback or not space or not timer_state:
        self._stop_event.wait(1)
        continue

      sleep_time = self._calculate_sleep_time(timer_state)

      # interruptible sleep
      if self._stop_event.wait(sleep_time):
        break

      if callback and space and timer_state and not self._stop_event.is_set():
        callback(space)

  def _calculate_sleep_time(self, timer_state: TimerState) -> float:
    """Calculate how long to sleep before next check based on time left."""
    remaining_time_sec = timer_state.get_remaining_time_ms() / 1000.0
    return max(0.01, remaining_time_sec)

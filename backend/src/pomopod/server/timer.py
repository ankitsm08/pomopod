import threading
import time
from typing import Callable, Optional

from pomopod.core.models import Space, TimerState


class TimerManager:
  def __init__(self):
    self._timer = None
    self._running = False
    self._callback: Optional[Callable[[Space], None]] = None
    self._space: Optional[Space] = None
    self._timer_state: Optional[TimerState] = None
    self._lock = threading.Lock()

  def change_space(self, space: Space) -> None:
    """Change space for timer."""
    with self._lock:
      self._space = space

  def start(self, callback: Callable[[Space], None], space: Space, timer_state: TimerState):
    """Start the background timer with a callback function."""
    with self._lock:
      self._callback = callback
      self._space = space
      self._timer_state = timer_state
      self._running = True
      self._timer = threading.Thread(target=self._run_loop, daemon=True)
      self._timer.start()

  def stop(self):
    """Stop the background timer."""
    with self._lock:
      self._running = False
      if self._timer:
        self._timer.join(timeout=2)

  def _run_loop(self):
    """Main loop that runs in background thread."""
    while True:
      with self._lock:
        if not self._running:
          break

        # get current state
        callback = self._callback
        space = self._space
        timer_state = self._timer_state
        running = self._running

      if not running or not callback or not space or not timer_state:
        time.sleep(1)
        continue

      sleep_time = self._calculate_sleep_time(timer_state)
      time.sleep(sleep_time)

      with self._lock:
        if self._running and self._callback and self._space and self._timer_state:
          self._callback(self._space)

  def _calculate_sleep_time(self, timer_state: TimerState) -> float:
    """Calculate how long to sleep before next check based on time left."""
    remaining_time_sec = timer_state.get_remaining_time_ms() / 1000.0
    return max(0.01, remaining_time_sec / 2)

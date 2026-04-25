import { DEFAULT_TIMER_SETTINGS, MILLISECONDS_PER_SECOND } from "./constants";
import type { PomodoroSessionId, TimerSettings } from "./types";

function padTimeUnit(value: number) {
  return String(value).padStart(2, "0");
}

export function clampTimerSettings(
  settings: Partial<TimerSettings>,
): TimerSettings {
  return {
    focus:
      typeof settings.focus === "number"
        ? Math.min(600, Math.max(1, settings.focus))
        : DEFAULT_TIMER_SETTINGS.focus,
    shortBreak:
      typeof settings.shortBreak === "number"
        ? settings.shortBreak
        : DEFAULT_TIMER_SETTINGS.shortBreak,
    longBreak:
      typeof settings.longBreak === "number"
        ? settings.longBreak
        : DEFAULT_TIMER_SETTINGS.longBreak,
    longBreakAfter:
      typeof settings.longBreakAfter === "number"
        ? Math.min(8, Math.max(2, settings.longBreakAfter))
        : DEFAULT_TIMER_SETTINGS.longBreakAfter,
  };
}

export function getTimeParts(totalMilliseconds: number) {
  const totalSeconds = Math.ceil(
    Math.max(totalMilliseconds, 0) / MILLISECONDS_PER_SECOND,
  );
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds / 60) % 60);
  const seconds = totalSeconds % 60;

  return {
    hours: padTimeUnit(hours),
    minutes: padTimeUnit(minutes),
    seconds: padTimeUnit(seconds),
  };
}

export function getSessionLength(
  session: PomodoroSessionId,
  settings: TimerSettings,
) {
  if (session === "focus") {
    return settings.focus;
  }

  if (session === "shortBreak") {
    return settings.shortBreak;
  }

  return settings.longBreak;
}

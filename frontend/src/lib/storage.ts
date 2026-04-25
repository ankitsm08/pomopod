import {
  DEFAULT_TIMER_SETTINGS,
  THEME_STORAGE_KEY,
  TIMER_SETTINGS_STORAGE_KEY,
} from "./constants";
import { clampTimerSettings } from "./timer";
import type { ThemeMode, TimerSettings } from "./types";

export function getInitialTheme(): ThemeMode {
  if (typeof window === "undefined") {
    return "light";
  }

  const storedTheme = window.localStorage.getItem(THEME_STORAGE_KEY);

  if (storedTheme === "light" || storedTheme === "dark") {
    return storedTheme;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export function getInitialTimerSettings(): TimerSettings {
  if (typeof window === "undefined") {
    return DEFAULT_TIMER_SETTINGS;
  }

  const storedSettings = window.localStorage.getItem(
    TIMER_SETTINGS_STORAGE_KEY,
  );

  if (!storedSettings) {
    return DEFAULT_TIMER_SETTINGS;
  }

  try {
    return clampTimerSettings(
      JSON.parse(storedSettings) as Partial<TimerSettings>,
    );
  } catch {
    return DEFAULT_TIMER_SETTINGS;
  }
}

import { BookOpenText, Code, UserRound } from "lucide-react";

import type { PomodoroSessionId, SpaceId, TimerSettings } from "./types";

export const THEME_STORAGE_KEY = "pomopod-theme";
export const TIMER_SETTINGS_STORAGE_KEY = "pomopod-timer-settings";
export const ROOM_CODE = "eur-towers-museums-personal";

export const MILLISECONDS_PER_SECOND = 1000;
export const MILLISECONDS_PER_MINUTE = 60 * MILLISECONDS_PER_SECOND;
export const TIMER_TICK_MS = 100;

export const DEFAULT_TIMER_SETTINGS: TimerSettings = {
  focus: 30,
  shortBreak: 5,
  longBreak: 15,
  longBreakAfter: 4,
};

export const POMODORO_NOTIFICATION_TRIGGER_SECONDS = 5;

export const SESSIONS: Array<{
  id: PomodoroSessionId;
  label: string;
}> = [
  { id: "focus", label: "Focus Mode" },
  { id: "shortBreak", label: "Short Break" },
  { id: "longBreak", label: "Long Break" },
];

export const SPACES: Array<{
  id: SpaceId;
  label: string;
  icon: typeof UserRound;
}> = [
  {
    id: "personal",
    label: "Personal",
    icon: UserRound,
  },
  {
    id: "coding",
    label: "Coding",
    icon: Code,
  },
  {
    id: "study",
    label: "Study",
    icon: BookOpenText,
  },
];

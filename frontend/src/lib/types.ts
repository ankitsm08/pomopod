export type PomodoroSessionId = "focus" | "shortBreak" | "longBreak";

export type ThemeMode = "light" | "dark";

export type SpaceId = "personal" | "study" | "coding";

export type TimerSettings = {
  focus: number;
  shortBreak: number;
  longBreak: number;
  longBreakAfter: number;
};

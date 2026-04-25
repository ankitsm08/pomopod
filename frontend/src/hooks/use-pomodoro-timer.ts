import { useEffect, useEffectEvent, useRef, useState } from "react";

import {
  MILLISECONDS_PER_MINUTE,
  TIMER_SETTINGS_STORAGE_KEY,
  TIMER_TICK_MS,
} from "@/lib/constants";
import { getInitialTimerSettings } from "@/lib/storage";
import { getSessionLength, getTimeParts } from "@/lib/timer";
import type { PomodoroSessionId, TimerSettings } from "@/lib/types";
import { usePomodoroEndingNotification } from "./use-pomodoro-ending-notification";

export function usePomodoroTimer() {
  const [activeSession, setActiveSession] =
    useState<PomodoroSessionId>("focus");
  const [completedFocusRounds, setCompletedFocusRounds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [timerSettings, setTimerSettings] = useState<TimerSettings>(
    getInitialTimerSettings,
  );
  const [timeLeft, setTimeLeft] = useState(
    () => getInitialTimerSettings().focus * MILLISECONDS_PER_MINUTE,
  );
  const timeLeftRef = useRef(timeLeft);

  const currentSessionLength = getSessionLength(activeSession, timerSettings);
  const currentSessionLengthInMs =
    currentSessionLength * MILLISECONDS_PER_MINUTE;
  const progressWidth =
    ((currentSessionLengthInMs - timeLeft) / currentSessionLengthInMs) * 100;
  const timeParts = getTimeParts(timeLeft);

  useEffect(() => {
    timeLeftRef.current = timeLeft;
  }, [timeLeft]);

  usePomodoroEndingNotification({
    activeSession,
    isRunning,
    timeLeft,
  });

  const switchSession = (
    session: PomodoroSessionId,
    settings = timerSettings,
    options?: {
      autoStart?: boolean;
    },
  ) => {
    const nextTime =
      getSessionLength(session, settings) * MILLISECONDS_PER_MINUTE;

    setActiveSession(session);
    setIsRunning(options?.autoStart ?? false);
    timeLeftRef.current = nextTime;
    setTimeLeft(nextTime);
  };

  const updateTimerSetting = (setting: keyof TimerSettings, value: number) => {
    const nextSettings = {
      ...timerSettings,
      [setting]: value,
    };

    setTimerSettings(nextSettings);

    if (
      (setting === "focus" ||
        setting === "shortBreak" ||
        setting === "longBreak") &&
      activeSession === setting
    ) {
      const nextTime = value * MILLISECONDS_PER_MINUTE;

      setIsRunning(false);
      timeLeftRef.current = nextTime;
      setTimeLeft(nextTime);
    }
  };

  const handleSessionComplete = useEffectEvent(() => {
    if (activeSession === "focus") {
      const nextRounds = completedFocusRounds + 1;
      const nextSession =
        nextRounds % timerSettings.longBreakAfter === 0
          ? "longBreak"
          : "shortBreak";

      setCompletedFocusRounds(nextRounds);
      switchSession(nextSession, timerSettings, { autoStart: true });

      return;
    }

    switchSession("focus", timerSettings, { autoStart: true });
  });

  useEffect(() => {
    window.localStorage.setItem(
      TIMER_SETTINGS_STORAGE_KEY,
      JSON.stringify(timerSettings),
    );
  }, [timerSettings]);

  useEffect(() => {
    if (!isRunning) {
      return;
    }

    let lastTick = window.performance.now();

    const timer = window.setInterval(() => {
      const now = window.performance.now();
      const elapsed = now - lastTick;
      lastTick = now;

      const nextTime = Math.max(0, timeLeftRef.current - elapsed);
      timeLeftRef.current = nextTime;
      setTimeLeft(nextTime);

      if (nextTime <= 0) {
        window.clearInterval(timer);
        handleSessionComplete();
      }
    }, TIMER_TICK_MS);

    return () => {
      window.clearInterval(timer);
    };
  }, [activeSession, isRunning]);

  const toggleTimer = () => {
    setIsRunning((current) => !current);
  };

  const resetTimer = () => {
    setIsRunning(false);
    timeLeftRef.current = currentSessionLengthInMs;
    setTimeLeft(currentSessionLengthInMs);
  };

  return {
    activeSession,
    completedFocusRounds,
    currentSessionLengthInMs,
    isRunning,
    progressWidth,
    switchSession,
    timeParts,
    timerSettings,
    toggleTimer,
    resetTimer,
    updateTimerSetting,
  };
}

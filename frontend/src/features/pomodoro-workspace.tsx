import { useState } from "react";

import { usePomodoroTimer } from "@/hooks/use-pomodoro-timer";
import { useRoomCodeClipboard } from "@/hooks/use-room-code-clipboard";
import { useThemeMode } from "@/hooks/use-theme-mode";

import { SPACES } from "@/lib/constants";
import type { SpaceId } from "@/lib/types";

import { PomodoroSettingsSheet } from "./pomodoro-settings-sheet";
import { PomodoroToaster } from "./pomodoro-toaster";
import { RoomCodePill } from "./room-code-pill";
import { SessionSelector } from "./session-selector-buttons";
import { SessionSummary } from "./session-summary";
import { SpaceSwitcher } from "./space-switcher-dock";
import { TimerActions } from "./timer-actions-buttons";
import { TimerDisplay } from "./timer-display";

export function PomodoroWorkspace() {
  const [activeSpace, setActiveSpace] = useState<SpaceId>("coding");
  const { theme, setTheme } = useThemeMode();
  const { isRoomCodeCopied, copyRoomCode } = useRoomCodeClipboard();
  const timer = usePomodoroTimer();
  const activeSpaceMeta =
    SPACES.find((space) => space.id === activeSpace) ?? SPACES[0];

  return (
    <>
      <div className="min-h-svh bg-background text-foreground">
        <div className="mx-auto flex min-h-svh w-full max-w-480 items-center justify-center overflow-hidden p-3 sm:p-4 lg:p-5 min-[1800px]:max-w-640">
          <section className="relative max-h-312 min-h-168 w-full overflow-hidden rounded-[2rem] border border-border/70 bg-card shadow-2xl">
            <div className="relative flex h-full min-h-168 flex-col p-4 sm:p-5 lg:p-6">
              <header className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-medium uppercase tracking-[0.24em] text-muted-foreground">
                    Pomopod
                  </p>
                  <h1 className="mt-2 text-xl font-semibold tracking-tight sm:text-2xl">
                    Pomodoro Workspace
                  </h1>
                </div>

                <PomodoroSettingsSheet
                  theme={theme}
                  timerSettings={timer.timerSettings}
                  onThemeChange={setTheme}
                  onSettingChange={timer.updateTimerSetting}
                />
              </header>

              <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center justify-center gap-5 py-5 sm:py-6 min-[1800px]:max-w-336">
                <div className="mt-10 w-full max-w-5xl text-center min-[1800px]:max-w-6xl">
                  <h2 className="mt-4 text-balance text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">
                    {activeSpaceMeta.label}
                  </h2>
                  <p className="mx-auto mt-2 max-w-2xl text-pretty text-sm leading-6 text-muted-foreground sm:text-base">
                    Code that communicates its purpose is very important.
                  </p>

                  <SessionSelector
                    activeSession={timer.activeSession}
                    onSessionChange={timer.switchSession}
                  />
                  <TimerDisplay
                    hours={timer.timeParts.hours}
                    minutes={timer.timeParts.minutes}
                    seconds={timer.timeParts.seconds}
                    progressWidth={timer.progressWidth}
                  />
                  <TimerActions
                    isRunning={timer.isRunning}
                    onToggle={timer.toggleTimer}
                    onReset={timer.resetTimer}
                  />
                </div>

                <RoomCodePill
                  isCopied={isRoomCodeCopied}
                  onCopy={() => {
                    void copyRoomCode();
                  }}
                />
              </div>

              <footer className="mt-auto flex flex-col gap-3 pt-4 md:flex-row md:items-end md:justify-between">
                <SessionSummary
                  completedFocusRounds={timer.completedFocusRounds}
                />
                <SpaceSwitcher
                  activeSpace={activeSpace}
                  onSpaceChange={setActiveSpace}
                />
              </footer>
            </div>
          </section>
        </div>
      </div>

      <PomodoroToaster theme={theme} />
    </>
  );
}

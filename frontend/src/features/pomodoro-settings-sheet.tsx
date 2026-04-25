import { MoonStar, Settings2, SunMedium } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import type { ThemeMode, TimerSettings } from "@/lib/types";

type TimerSettingSliderProps = {
  description: string;
  label: string;
  max: number;
  onChange: (value: number) => void;
  suffix: string;
  value: number;
};

type PomodoroSettingsSheetProps = {
  onSettingChange: (setting: keyof TimerSettings, value: number) => void;
  onThemeChange: (theme: ThemeMode) => void;
  theme: ThemeMode;
  timerSettings: TimerSettings;
};

function TimerSettingSlider({
  description,
  label,
  max,
  onChange,
  suffix,
  value,
}: TimerSettingSliderProps) {
  return (
    <div>
      <div className="flex items-center justify-between gap-4">
        <div>
          <h3 className="font-medium">{label}</h3>
          <p className="mt-1 text-sm text-muted-foreground">{description}</p>
        </div>

        <span className="shrink-0 whitespace-nowrap rounded-full border border-border bg-muted px-3 py-1 text-sm font-medium">
          {value} {suffix}
        </span>
      </div>

      <Slider
        className="mt-4"
        min={1}
        max={Math.cbrt(max)}
        step={0.001}
        value={[Math.cbrt(value)]}
        onValueChange={([nextValue]) => {
          onChange(Math.round(Math.pow(nextValue, 3)));
        }}
      />
    </div>
  );
}

export function PomodoroSettingsSheet({
  onSettingChange,
  onThemeChange,
  theme,
  timerSettings,
}: PomodoroSettingsSheetProps) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          aria-label="Open pomodoro settings"
          className="rounded-full bg-background/80 backdrop-blur"
        >
          <Settings2 />
        </Button>
      </SheetTrigger>

      <SheetContent className="w-full sm:max-w-md">
        <SheetHeader>
          <SheetTitle className="mt-10 font-semibold text-3xl">
            Settings
          </SheetTitle>
          <SheetDescription>
            Adjust focus and break lengths, then switch between light and dark
            mode.
          </SheetDescription>
        </SheetHeader>

        <div className="space-y-6 px-4 pb-6">
          <section className="rounded-3xl border border-border bg-card p-5">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h3 className="font-medium">Appearance</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Dark mode / Light mode
                </p>
              </div>

              <div className="flex items-center gap-3">
                <SunMedium className="size-4 text-muted-foreground" />
                <Switch
                  checked={theme === "dark"}
                  onCheckedChange={(checked) => {
                    onThemeChange(checked ? "dark" : "light");
                  }}
                  aria-label="Toggle dark mode"
                />
                <MoonStar className="size-4 text-muted-foreground" />
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-border bg-card p-5">
            <div className="space-y-5">
              <TimerSettingSlider
                label="Focus timer"
                description="How long a focus session should run."
                value={timerSettings.focus}
                suffix="min"
                max={600}
                onChange={(value) => {
                  onSettingChange("focus", value);
                }}
              />
              <TimerSettingSlider
                label="Short break"
                description="Quick reset after a focus round."
                value={timerSettings.shortBreak}
                suffix="min"
                max={120}
                onChange={(value) => {
                  onSettingChange("shortBreak", value);
                }}
              />
              <TimerSettingSlider
                label="Long break"
                description="Longer recovery after four focus rounds."
                value={timerSettings.longBreak}
                suffix="min"
                max={300}
                onChange={(value) => {
                  onSettingChange("longBreak", value);
                }}
              />
              <TimerSettingSlider
                label="Long break trigger"
                description="Choose how many focus sessions happen before a long break."
                value={timerSettings.longBreakAfter}
                suffix="sessions"
                max={25}
                onChange={(value) => {
                  onSettingChange("longBreakAfter", value);
                }}
              />
            </div>
          </section>
        </div>
      </SheetContent>
    </Sheet>
  );
}

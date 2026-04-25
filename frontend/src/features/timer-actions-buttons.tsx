import { Pause, Play, RotateCcw, Square } from "lucide-react";

import { Button } from "@/components/ui/button";

type TimerActionsProps = {
  isRunning: boolean;
  onReset: () => void;
  onToggle: () => void;
};

export function TimerActions({
  isRunning,
  onReset,
  onToggle,
}: TimerActionsProps) {
  return (
    <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
      <Button size="lg" className="rounded-full px-6" onClick={onToggle}>
        {isRunning ? <Pause /> : <Play />}
        {isRunning ? "Pause" : "Start"}
      </Button>

      <Button
        size="lg"
        variant="outline"
        className="rounded-full px-6"
        onClick={onReset}
      >
        <RotateCcw />
        Reset
      </Button>

      <Button
        size="lg"
        variant="outline"
        className="rounded-full px-6"
        onClick={onReset}
      >
        <Square />
        Stop
      </Button>
    </div>
  );
}

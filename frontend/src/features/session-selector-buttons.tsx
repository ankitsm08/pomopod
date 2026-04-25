import { Button } from "@/components/ui/button";
import { SESSIONS } from "@/lib/constants";
import type { PomodoroSessionId } from "@/lib/types";

type SessionSelectorProps = {
  activeSession: PomodoroSessionId;
  onSessionChange: (session: PomodoroSessionId) => void;
};

export function SessionSelector({
  activeSession,
  onSessionChange,
}: SessionSelectorProps) {
  return (
    <div className="mt-6 flex flex-wrap justify-center gap-3">
      {SESSIONS.map((session) => (
        <Button
          key={session.id}
          variant={session.id === activeSession ? "default" : "outline"}
          className="rounded-full px-5"
          onClick={() => {
            onSessionChange(session.id);
          }}
        >
          {session.label}
        </Button>
      ))}
    </div>
  );
}

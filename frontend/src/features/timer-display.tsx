type TimerDisplayProps = {
  hours: string;
  minutes: string;
  progressWidth: number;
  seconds: string;
};

export function TimerDisplay({
  hours,
  minutes,
  progressWidth,
  seconds,
}: TimerDisplayProps) {
  return (
    <>
      <div className="mt-6 flex items-start justify-center text-[clamp(4rem,14vw,9rem)] font-semibold leading-none tracking-[-0.06em] tabular-nums">
        {Number.parseInt(hours) > 0 && (
          <>
            <span>{hours}</span>
            <span className="relative -top-[0.1em] mx-[0.04em]">{":"}</span>
          </>
        )}
        <span>{minutes}</span>
        <span className="relative -top-[0.1em] mx-[0.04em]">{":"}</span>
        <span>{seconds}</span>
      </div>

      <div className="mx-auto mt-6 max-w-lg rounded-full border border-border bg-background/80 p-2 backdrop-blur">
        <div className="h-2 rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-primary transition-[width]"
            style={{
              width: `${Number.isFinite(progressWidth) ? progressWidth : 0}%`,
            }}
          />
        </div>
      </div>
    </>
  );
}

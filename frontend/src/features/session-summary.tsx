type SessionSummaryProps = {
  completedFocusRounds: number;
};

export function SessionSummary({ completedFocusRounds }: SessionSummaryProps) {
  return (
    <div className="w-full max-w-xs rounded-3xl border border-border bg-background/80 p-4 pr-10 backdrop-blur md:w-auto">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">
        Session flow
      </p>
      <p className="mt-1.5 text-base font-semibold">
        {completedFocusRounds} rounds completed
      </p>
    </div>
  );
}

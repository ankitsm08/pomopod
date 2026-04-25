import { Toaster } from "sonner";

import type { ThemeMode } from "@/lib/types";

type PomodoroToasterProps = {
  theme: ThemeMode;
};

export function PomodoroToaster({ theme }: PomodoroToasterProps) {
  return (
    <Toaster
      theme={theme}
      position="bottom-center"
      style={
        {
          "--width": "18rem",
        } as React.CSSProperties
      }
      toastOptions={{
        unstyled: true,
        classNames: {
          toast:
            "mb-15 flex w-full min-h-0 items-center justify-center rounded-full border border-border bg-background/80 px-4 py-4 text-center text-muted-foreground shadow-md",
          content: "flex w-full flex-nowrap items-center justify-center gap-2",
          icon: "shrink-0",
          title:
            "ml-1 text-xs font-medium leading-none tracking-[0.16em] uppercase text-muted-foreground",
        },
      }}
    />
  );
}

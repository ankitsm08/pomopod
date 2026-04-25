import { startTransition } from "react";

import { buttonVariants } from "@/components/ui/button";
import { Dock, DockIcon } from "@/components/ui/dock";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { SPACES } from "@/lib/constants";
import type { SpaceId } from "@/lib/types";
import { cn } from "@/lib/utils";

type SpaceSwitcherProps = {
  activeSpace: SpaceId;
  onSpaceChange: (space: SpaceId) => void;
};

export function SpaceSwitcher({
  activeSpace,
  onSpaceChange,
}: SpaceSwitcherProps) {
  return (
    <div className="ml-auto flex flex-col items-center justify-center gap-2">
      <p className="rounded-full border border-border bg-background/80 px-4 py-2 text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground backdrop-blur">
        Switch spaces
      </p>

      <TooltipProvider>
        <Dock
          direction="middle"
          className="mt-0 self-end border-border bg-background/80"
          iconSize={42}
          iconMagnification={58}
        >
          {SPACES.map(({ id, label, icon: Icon }) => {
            const isActive = activeSpace === id;

            return (
              <DockIcon key={id}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button
                      type="button"
                      aria-label={`Switch to ${label} space`}
                      className={cn(
                        buttonVariants({
                          variant: "ghost",
                          size: "icon",
                        }),
                        "size-12 rounded-full border border-transparent p-0",
                      )}
                      onClick={() => {
                        startTransition(() => {
                          onSpaceChange(id);
                        });
                      }}
                    >
                      <span
                        className={cn(
                          "flex size-10 items-center justify-center rounded-full transition-colors",
                          isActive &&
                            "bg-accent text-accent-foreground shadow-sm",
                        )}
                      >
                        <Icon className="size-4" />
                      </span>
                    </button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{label}</p>
                  </TooltipContent>
                </Tooltip>
              </DockIcon>
            );
          })}
        </Dock>
      </TooltipProvider>
    </div>
  );
}

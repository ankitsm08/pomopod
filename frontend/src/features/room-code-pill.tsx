import { Check, Copy } from "lucide-react";

import { Button } from "@/components/ui/button";
import { ROOM_CODE } from "@/lib/constants";

type RoomCodePillProps = {
  isCopied: boolean;
  onCopy: () => void;
};

export function RoomCodePill({ isCopied, onCopy }: RoomCodePillProps) {
  return (
    <div className="mt-3 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
      <div className="flex items-center gap-2 rounded-full border border-border bg-background/80 px-3 py-2 backdrop-blur">
        <span className="ml-2">{ROOM_CODE}</span>
        <Button
          type="button"
          variant="ghost"
          size="icon-sm"
          className="rounded-full text-muted-foreground hover:bg-muted/80 hover:text-foreground"
          onClick={onCopy}
        >
          {isCopied ? <Check /> : <Copy />}
        </Button>
      </div>
    </div>
  );
}

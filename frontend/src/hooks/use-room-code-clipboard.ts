import { useState } from "react";

import { ROOM_CODE } from "@/lib/constants";

export function useRoomCodeClipboard() {
  const [isRoomCodeCopied, setIsRoomCodeCopied] = useState(false);

  const copyRoomCode = async () => {
    try {
      await navigator.clipboard.writeText(ROOM_CODE);
      setIsRoomCodeCopied(true);

      window.setTimeout(() => {
        setIsRoomCodeCopied(false);
      }, 2000);
    } catch {
      setIsRoomCodeCopied(false);
    }
  };

  return {
    isRoomCodeCopied,
    copyRoomCode,
  };
}

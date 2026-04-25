import { useEffect, useState } from "react";

import { THEME_STORAGE_KEY } from "@/lib/constants";
import { getInitialTheme } from "@/lib/storage";
import type { ThemeMode } from "@/lib/types";

export function useThemeMode() {
  const [theme, setTheme] = useState<ThemeMode>(getInitialTheme);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    window.localStorage.setItem(THEME_STORAGE_KEY, theme);
  }, [theme]);

  return {
    theme,
    setTheme,
  };
}

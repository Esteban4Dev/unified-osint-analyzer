import { createContext, useContext, useState, useMemo, useEffect } from "react";
import { translations, LANGUAGES } from "../i18n/translations";

const LanguageContext = createContext(null);

function detectInitialLanguage() {
  const stored = window.localStorage.getItem("osint-dashboard-lang");
  if (stored && LANGUAGES.includes(stored)) return stored;
  const browserLang = navigator.language?.slice(0, 2);
  return LANGUAGES.includes(browserLang) ? browserLang : "es";
}

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(detectInitialLanguage);

  useEffect(() => {
    window.localStorage.setItem("osint-dashboard-lang", lang);
  }, [lang]);

  const value = useMemo(
    () => ({
      lang,
      setLang,
      t: (key) => translations[lang][key] ?? key,
    }),
    [lang]
  );

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage debe usarse dentro de LanguageProvider");
  return ctx;
}

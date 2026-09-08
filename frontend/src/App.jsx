import { useState } from "react";
import Home from "./pages/Home";
import History from "./pages/History";
import { useLanguage } from "./context/LanguageContext";

export default function App() {
  const [page, setPage] = useState("home");
  const { lang, setLang, t } = useLanguage();

  return (
    <div className="min-h-screen bg-slate-950">
      <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex gap-4">
            <button
              onClick={() => setPage("home")}
              className={`text-sm font-medium ${
                page === "home" ? "text-cyan-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t("navSearch")}
            </button>
            <button
              onClick={() => setPage("history")}
              className={`text-sm font-medium ${
                page === "history" ? "text-cyan-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t("navHistory")}
            </button>
          </div>

          <div className="flex rounded-lg border border-slate-700 overflow-hidden text-xs font-medium">
            <button
              onClick={() => setLang("es")}
              className={`px-3 py-1.5 transition-colors ${
                lang === "es" ? "bg-cyan-600 text-white" : "text-slate-400 hover:bg-slate-800"
              }`}
            >
              ES
            </button>
            <button
              onClick={() => setLang("en")}
              className={`px-3 py-1.5 transition-colors ${
                lang === "en" ? "bg-cyan-600 text-white" : "text-slate-400 hover:bg-slate-800"
              }`}
            >
              EN
            </button>
          </div>
        </div>
      </nav>

      {page === "home" ? <Home /> : <History />}
    </div>
  );
}

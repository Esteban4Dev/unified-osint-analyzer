import { useEffect, useState } from "react";
import SearchBar from "./SearchBar";
import ResultsTable from "./ResultsTable";
import RelationshipGraph from "./RelationshipGraph";
import TechBadge from "./TechBadge";
import { useOSINT } from "../hooks/useOSINT";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";

export default function Dashboard() {
  const { search, result, loading, error } = useOSINT();
  const { t } = useLanguage();
  const [sources, setSources] = useState(null);

  useEffect(() => {
    api.getSources().then(setSources).catch(() => {});
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-slate-100">{t("appTitle")}</h1>
        <p className="text-sm text-slate-500 mt-1">{t("appSubtitle")}</p>
        {sources && (
          <div className="flex flex-wrap gap-2 mt-4">
            {Object.entries(sources).map(([source, configured]) => (
              <TechBadge key={source} source={source} configured={configured} />
            ))}
          </div>
        )}
      </header>

      <SearchBar onSearch={search} loading={loading} />

      {error && (
        <p className="mt-4 text-sm text-red-400 bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-3">
          {error}
        </p>
      )}

      {result && (
        <div className="mt-6 grid gap-6 md:grid-cols-[1fr_320px]">
          <ResultsTable record={result} />
          <RelationshipGraph record={result} />
        </div>
      )}
    </div>
  );
}

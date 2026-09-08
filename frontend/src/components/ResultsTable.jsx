import TechBadge from "./TechBadge";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";

export default function ResultsTable({ record }) {
  const { t } = useLanguage();
  if (!record) return null;

  const { id, query, query_type: queryType, result } = record;

  return (
    <div className="mt-6 space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">{query}</h2>
          <p className="text-xs text-slate-500 uppercase tracking-wide">{queryType}</p>
        </div>
        <div className="flex gap-2">
          <a
            href={api.reportUrl(id, "json")}
            className="text-xs px-3 py-1.5 rounded-md border border-slate-700 hover:bg-slate-800 transition-colors"
          >
            {t("exportJson")}
          </a>
          <a
            href={api.reportUrl(id, "pdf")}
            className="text-xs px-3 py-1.5 rounded-md border border-slate-700 hover:bg-slate-800 transition-colors"
          >
            {t("exportPdf")}
          </a>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {Object.entries(result).map(([source, data]) => (
          <div
            key={source}
            className="rounded-xl border border-slate-800 bg-slate-900/50 p-4"
          >
            <div className="mb-3">
              <TechBadge source={source} configured={data.configured} />
            </div>
            {data.error ? (
              <p className="text-sm text-amber-400">{data.error}</p>
            ) : (
              <pre className="text-xs text-slate-300 whitespace-pre-wrap break-words max-h-64 overflow-auto">
                {JSON.stringify(data, null, 2)}
              </pre>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

import { useEffect, useState } from "react";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";

export default function History() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const { t } = useLanguage();

  useEffect(() => {
    api
      .getHistory()
      .then(setItems)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold text-slate-100 mb-6">{t("historyTitle")}</h1>

      {loading && <p className="text-sm text-slate-500">{t("historyLoading")}</p>}

      {!loading && items.length === 0 && (
        <p className="text-sm text-slate-500">{t("historyEmpty")}</p>
      )}

      <div className="space-y-2">
        {items.map((item) => (
          <div
            key={item.id}
            className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-900/50 px-4 py-3"
          >
            <div>
              <p className="text-sm font-medium text-slate-200">{item.query}</p>
              <p className="text-xs text-slate-500">
                {item.query_type} · {new Date(item.created_at).toLocaleString()}
              </p>
            </div>
            <div className="flex gap-2">
              <a
                href={api.reportUrl(item.id, "json")}
                className="text-xs px-3 py-1.5 rounded-md border border-slate-700 hover:bg-slate-800"
              >
                JSON
              </a>
              <a
                href={api.reportUrl(item.id, "pdf")}
                className="text-xs px-3 py-1.5 rounded-md border border-slate-700 hover:bg-slate-800"
              >
                PDF
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

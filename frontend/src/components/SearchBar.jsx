import { useState } from "react";
import { useLanguage } from "../context/LanguageContext";

export default function SearchBar({ onSearch, loading }) {
  const [value, setValue] = useState("");
  const { t } = useLanguage();

  function handleSubmit(e) {
    e.preventDefault();
    if (!value.trim()) return;
    onSearch(value.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={t("searchPlaceholder")}
        className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
      />
      <button
        type="submit"
        disabled={loading}
        className="px-5 py-3 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-sm font-medium transition-colors"
      >
        {loading ? t("searchButtonLoading") : t("searchButton")}
      </button>
    </form>
  );
}

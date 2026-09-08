import { useState, useCallback } from "react";
import { api } from "../services/api";
import { useLanguage } from "../context/LanguageContext";

export function useOSINT() {
  const { lang } = useLanguage();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const search = useCallback(
    async (query) => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.search(query, lang);
        setResult(data);
        return data;
      } catch (err) {
        setError(err.message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [lang]
  );

  return { search, result, loading, error };
}

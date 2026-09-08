/**
 * Grafo de relaciones simple: nodo central (la consulta) conectado a cada
 * fuente que devolvió datos. Implementado con SVG puro para no añadir
 * dependencias pesadas (D3/Vis.js) en esta primera versión.
 *
 * Próximo paso sugerido: sustituir por D3.js o Vis.js si se necesita
 * mostrar relaciones entre múltiples entidades (no solo consulta -> fuente).
 */
import { useLanguage } from "../context/LanguageContext";

export default function RelationshipGraph({ record }) {
  const { t } = useLanguage();
  if (!record) return null;

  const sources = Object.keys(record.result);
  const centerX = 200;
  const centerY = 150;
  const radius = 110;

  const nodes = sources.map((source, i) => {
    const angle = (2 * Math.PI * i) / sources.length - Math.PI / 2;
    return {
      source,
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
      ok: !record.result[source].error,
    };
  });

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
      <p className="text-xs text-slate-500 mb-2">{t("relationshipMap")}</p>
      <svg viewBox="0 0 400 300" className="w-full h-64">
        {nodes.map((n) => (
          <line
            key={`line-${n.source}`}
            x1={centerX}
            y1={centerY}
            x2={n.x}
            y2={n.y}
            stroke={n.ok ? "#22d3ee" : "#475569"}
            strokeWidth="1.5"
          />
        ))}

        <circle cx={centerX} cy={centerY} r="26" fill="#0891b2" />
        <text
          x={centerX}
          y={centerY + 4}
          textAnchor="middle"
          fontSize="10"
          fill="white"
        >
          {record.query.length > 12 ? record.query.slice(0, 10) + "…" : record.query}
        </text>

        {nodes.map((n) => (
          <g key={n.source}>
            <circle cx={n.x} cy={n.y} r="20" fill={n.ok ? "#059669" : "#334155"} />
            <text x={n.x} y={n.y + 4} textAnchor="middle" fontSize="9" fill="white">
              {n.source}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
}

const COLORS = {
  shodan: "bg-red-500/15 text-red-400 border-red-500/30",
  virustotal: "bg-blue-500/15 text-blue-400 border-blue-500/30",
  hibp: "bg-orange-500/15 text-orange-400 border-orange-500/30",
  securitytrails: "bg-purple-500/15 text-purple-400 border-purple-500/30",
  dns: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
};

export default function TechBadge({ source, configured }) {
  const color = COLORS[source] || "bg-slate-500/15 text-slate-400 border-slate-500/30";
  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium border ${color}`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full ${
          configured ? "bg-emerald-400" : "bg-slate-500"
        }`}
      />
      {source}
    </span>
  );
}

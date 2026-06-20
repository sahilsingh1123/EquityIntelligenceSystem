export function label(value: string): string {
  return value
    .toLowerCase()
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function toneClass(value: string): string {
  if (value === "POSITIVE") return "text-gain bg-emerald-50 border-emerald-200";
  if (value === "NEGATIVE") return "text-loss bg-red-50 border-red-200";
  if (value === "UNCERTAIN") return "text-caution bg-amber-50 border-amber-200";
  return "text-ink bg-slate-50 border-slate-200";
}

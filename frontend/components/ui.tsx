import { clsx } from "clsx";
import type { ReactNode } from "react";

export function Panel({
  title,
  action,
  children,
  className
}: {
  title: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={clsx("rounded-lg border border-line bg-white shadow-soft", className)}>
      <header className="flex min-h-12 items-center justify-between border-b border-line px-4 py-3">
        <h2 className="text-sm font-semibold uppercase tracking-normal text-slate-700">{title}</h2>
        {action}
      </header>
      <div className="p-4">{children}</div>
    </section>
  );
}

export function ScoreBar({ value, tone = "info" }: { value: number; tone?: "info" | "gain" | "loss" }) {
  const color = tone === "gain" ? "bg-gain" : tone === "loss" ? "bg-loss" : "bg-info";
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
      <div className={clsx("h-full rounded-full", color)} style={{ width: `${value}%` }} />
    </div>
  );
}

export function Pill({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <span className={clsx("inline-flex items-center rounded-md border px-2 py-1 text-xs font-medium", className)}>
      {children}
    </span>
  );
}

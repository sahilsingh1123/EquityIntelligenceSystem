import { Activity, AlertTriangle, Bot, FileText, Globe2, Search, TrendingUp } from "lucide-react";
import type React from "react";

import { label, toneClass } from "@/lib/format";
import type { DashboardData } from "@/lib/types";
import { Panel, Pill, ScoreBar } from "@/components/ui";

export function Dashboard({ data }: { data: DashboardData }) {
  const positiveEvents = data.events.filter((event) => event.sentiment === "POSITIVE").length;
  const negativeEvents = data.events.filter((event) => event.sentiment === "NEGATIVE").length;
  const avgConfidence = Math.round(
    data.events.reduce((sum, event) => sum + event.confidence, 0) / Math.max(data.events.length, 1)
  );

  return (
    <main className="min-h-screen bg-[#eef3f7] text-ink">
      <div className="mx-auto flex max-w-[1440px] flex-col gap-4 px-4 py-4 lg:px-6">
        <header className="flex flex-col gap-3 border-b border-line pb-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-normal">AI Equity Intelligence</h1>
            <p className="mt-1 text-sm text-slate-600">
              Event-centric market intelligence for Indian equities with global context.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button className="inline-flex h-10 items-center gap-2 rounded-md border border-line bg-white px-3 text-sm font-medium shadow-soft">
              <Search size={16} /> Search
            </button>
            <button className="inline-flex h-10 items-center gap-2 rounded-md bg-ink px-3 text-sm font-medium text-white">
              <FileText size={16} /> Daily Report
            </button>
          </div>
        </header>

        <section className="grid metric-grid gap-3">
          <Metric icon={<Activity size={18} />} label="Structured Events" value={data.events.length.toString()} />
          <Metric icon={<TrendingUp size={18} />} label="Positive Signals" value={positiveEvents.toString()} />
          <Metric icon={<AlertTriangle size={18} />} label="Risk Events" value={negativeEvents.toString()} />
          <Metric icon={<Globe2 size={18} />} label="Avg Confidence" value={`${avgConfidence}%`} />
        </section>

        <section className="grid gap-4 xl:grid-cols-[1.3fr_0.9fr]">
          <Panel title="Market Pulse">
            <div className="grid gap-3 md:grid-cols-3">
              <PulseItem title="India" status="Primary market" detail="Events prioritized for Indian listed equities." />
              <PulseItem title="United States" status="Reference market" detail="Fed, tariffs, dollar and tech demand watched." />
              <PulseItem title="Japan" status="Reference market" detail="Rates, yen and supply-chain developments tracked." />
            </div>
          </Panel>
          <Panel title="Global Impact">
            <div className="space-y-3 text-sm">
              <Impact path="Oil Price Increase -> Transportation Costs -> Airlines -> Margins" confidence={82} />
              <Impact path="Federal Reserve -> Dollar Strength -> Indian IT -> Revenue Translation" confidence={76} />
              <Impact path="US Tariffs -> Electronics Manufacturing -> Indian EMS Companies" confidence={71} />
            </div>
          </Panel>
        </section>

        <section className="grid gap-4 xl:grid-cols-2">
          <Panel title="Top Opportunities">
            <div className="space-y-4">
              {data.opportunities.map((item) => (
                <ScoreRow key={item.opportunity_id} name={item.company_name} score={item.score} reason={item.reason} tone="gain" />
              ))}
            </div>
          </Panel>
          <Panel title="Top Risks">
            <div className="space-y-4">
              {data.risks.map((item) => (
                <ScoreRow key={item.risk_id} name={item.company_name} score={item.score} reason={item.reason} tone="loss" />
              ))}
            </div>
          </Panel>
        </section>

        <section className="grid gap-4 xl:grid-cols-[1fr_0.8fr]">
          <Panel title="Event Feed">
            <div className="space-y-3">
              {data.events.map((event) => (
                <article key={event.event_id} className="rounded-md border border-line p-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <strong className="text-sm">{event.company_name}</strong>
                    <Pill className={toneClass(event.sentiment)}>{label(event.event_type)}</Pill>
                    <span className="text-xs text-slate-500">{event.confidence}% confidence</span>
                  </div>
                  <p className="mt-2 text-sm text-slate-700">{event.summary}</p>
                  <p className="mt-2 text-xs text-slate-500">
                    Source: {event.evidence[0]?.source ?? "Unknown"} · {event.evidence[0]?.title ?? "No title"}
                  </p>
                </article>
              ))}
            </div>
          </Panel>

          <div className="grid gap-4">
            <Panel title="Company Explorer">
              <div className="space-y-3">
                {[...new Set(data.events.map((event) => event.company_name))].map((company) => (
                  <div key={company} className="flex items-center justify-between rounded-md border border-line p-3">
                    <span className="text-sm font-medium">{company}</span>
                    <Pill className="border-slate-200 bg-slate-50 text-slate-700">
                      {data.events.filter((event) => event.company_name === company).length} events
                    </Pill>
                  </div>
                ))}
              </div>
            </Panel>

            <Panel title="Conversational AI" action={<Bot size={18} className="text-info" />}>
              <div className="space-y-3">
                <div className="rounded-md border border-line bg-panel p-3 text-sm text-slate-700">
                  Ask evidence-backed questions such as “Which companies benefit from lower crude oil?”
                </div>
                <div className="flex gap-2">
                  <input
                    className="h-10 min-w-0 flex-1 rounded-md border border-line px-3 text-sm outline-none focus:border-info"
                    placeholder="Ask about events, risks, sectors..."
                  />
                  <button className="inline-flex h-10 items-center rounded-md bg-info px-3 text-sm font-medium text-white">
                    Ask
                  </button>
                </div>
              </div>
            </Panel>
          </div>
        </section>

        <Panel title="Daily Intelligence Report">
          <div className="grid gap-4 lg:grid-cols-3">
            {data.insights.map((insight) => (
              <article key={insight.insight_id} className="rounded-md border border-line p-3">
                <h3 className="text-sm font-semibold">{insight.title}</h3>
                <p className="mt-2 text-sm text-slate-700">{insight.why_it_matters}</p>
                <div className="mt-3">
                  <ScoreBar value={insight.confidence} />
                  <span className="mt-1 block text-xs text-slate-500">{insight.confidence}% confidence</span>
                </div>
              </article>
            ))}
          </div>
        </Panel>
      </div>
    </main>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex h-24 items-center gap-3 rounded-lg border border-line bg-white px-4 shadow-soft">
      <div className="grid h-10 w-10 place-items-center rounded-md bg-panel text-info">{icon}</div>
      <div>
        <div className="text-2xl font-semibold">{value}</div>
        <div className="text-xs uppercase tracking-normal text-slate-500">{label}</div>
      </div>
    </div>
  );
}

function PulseItem({ title, status, detail }: { title: string; status: string; detail: string }) {
  return (
    <div className="rounded-md border border-line p-3">
      <div className="text-sm font-semibold">{title}</div>
      <div className="mt-1 text-xs font-medium text-info">{status}</div>
      <p className="mt-2 text-sm text-slate-600">{detail}</p>
    </div>
  );
}

function Impact({ path, confidence }: { path: string; confidence: number }) {
  return (
    <div>
      <div className="flex items-center justify-between gap-3">
        <span>{path}</span>
        <span className="text-xs text-slate-500">{confidence}%</span>
      </div>
      <div className="mt-2">
        <ScoreBar value={confidence} />
      </div>
    </div>
  );
}

function ScoreRow({
  name,
  score,
  reason,
  tone
}: {
  name: string;
  score: number;
  reason: string;
  tone: "gain" | "loss";
}) {
  return (
    <article className="rounded-md border border-line p-3">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold">{name}</h3>
          <p className="mt-1 text-sm text-slate-600">{reason}</p>
        </div>
        <span className="text-lg font-semibold">{score}</span>
      </div>
      <div className="mt-3">
        <ScoreBar value={score} tone={tone} />
      </div>
    </article>
  );
}

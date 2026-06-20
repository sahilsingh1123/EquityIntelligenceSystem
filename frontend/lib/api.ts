import { demoData } from "@/lib/demo-data";
import type { DashboardData } from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { next: { revalidate: 15 } });
  if (!response.ok) {
    throw new Error(`API request failed: ${path}`);
  }
  return response.json() as Promise<T>;
}

export async function getDashboardData(): Promise<DashboardData> {
  try {
    const [events, opportunities, risks, insights] = await Promise.all([
      fetchJson<DashboardData["events"]>("/events"),
      fetchJson<DashboardData["opportunities"]>("/opportunities"),
      fetchJson<DashboardData["risks"]>("/risks"),
      fetchJson<DashboardData["insights"]>("/insights")
    ]);

    if (!events.length && !opportunities.length && !risks.length && !insights.length) {
      return demoData;
    }

    return { events, opportunities, risks, insights };
  } catch {
    return demoData;
  }
}

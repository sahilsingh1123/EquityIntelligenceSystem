export type Evidence = {
  source: string;
  title: string;
  excerpt: string;
  url?: string | null;
};

export type EventItem = {
  event_id: string;
  company_name: string;
  event_type: string;
  sentiment: "POSITIVE" | "NEGATIVE" | "NEUTRAL" | "UNCERTAIN";
  confidence: number;
  importance: number;
  summary: string;
  evidence: Evidence[];
};

export type Opportunity = {
  opportunity_id: string;
  company_name: string;
  score: number;
  confidence: number;
  reason: string;
};

export type Risk = {
  risk_id: string;
  company_name: string;
  score: number;
  confidence: number;
  reason: string;
};

export type Insight = {
  insight_id: string;
  title: string;
  what_happened: string;
  why_it_matters: string;
  potential_impact: string;
  confidence: number;
  importance: number;
  watch_points: string[];
  evidence: Evidence[];
};

export type DashboardData = {
  events: EventItem[];
  opportunities: Opportunity[];
  risks: Risk[];
  insights: Insight[];
};

import type { DashboardData } from "@/lib/types";

export const demoData: DashboardData = {
  events: [
    {
      event_id: "evt-1",
      company_name: "Infosys",
      event_type: "CONTRACT_WIN",
      sentiment: "POSITIVE",
      confidence: 95,
      importance: 90,
      summary: "Infosys contract win detected from NSE Filing.",
      evidence: [
        {
          source: "NSE Filing",
          title: "Infosys wins large cloud transformation contract",
          excerpt: "Infosys announced a large deal with a global manufacturer."
        }
      ]
    },
    {
      event_id: "evt-2",
      company_name: "ABC Bank",
      event_type: "REGULATORY_ACTION",
      sentiment: "NEGATIVE",
      confidence: 95,
      importance: 90,
      summary: "ABC Bank regulatory action detected from BSE Filing.",
      evidence: [
        {
          source: "BSE Filing",
          title: "ABC Bank receives regulatory action notice",
          excerpt: "The bank disclosed a show cause notice related to compliance processes."
        }
      ]
    },
    {
      event_id: "evt-3",
      company_name: "Indian Airlines",
      event_type: "MACRO_EVENT",
      sentiment: "UNCERTAIN",
      confidence: 85,
      importance: 90,
      summary: "Oil price increase may pressure Indian airline margins.",
      evidence: [
        {
          source: "Macro Desk",
          title: "Oil price increase raises pressure on airline margins",
          excerpt: "Higher crude can pressure transportation costs and airline margins."
        }
      ]
    }
  ],
  opportunities: [
    {
      opportunity_id: "opp-1",
      company_name: "Infosys",
      score: 74,
      confidence: 95,
      reason: "Detected positive catalysts: Contract Win."
    }
  ],
  risks: [
    {
      risk_id: "risk-1",
      company_name: "ABC Bank",
      score: 58,
      confidence: 95,
      reason: "Detected risk factors: Regulatory Action."
    },
    {
      risk_id: "risk-2",
      company_name: "Indian Airlines",
      score: 45,
      confidence: 85,
      reason: "Macro pressure from crude oil may affect margins."
    }
  ],
  insights: [
    {
      insight_id: "ins-1",
      title: "Infosys: Contract Win",
      what_happened: "Infosys announced a large contract win.",
      why_it_matters: "It improves revenue visibility and may support sentiment in IT services.",
      potential_impact: "Monitor deal ramp-up, margins, and peer read-throughs.",
      confidence: 95,
      importance: 90,
      watch_points: ["Filing confirmation", "Management commentary", "Peer reaction"],
      evidence: [
        {
          source: "NSE Filing",
          title: "Infosys wins large cloud transformation contract",
          excerpt: "Infosys announced an order win and large deal."
        }
      ]
    }
  ]
};

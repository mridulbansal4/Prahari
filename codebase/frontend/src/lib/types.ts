// DTOs mirroring the core API (Bible §7). snake_case fields as returned by the backend.
export type ConfidenceState = "grounded" | "inferred" | "unsupported" | "abstained";

export interface Citation {
  doc_id: string;
  page: number | null;
  span_id: string;
  excerpt: string | null;
}
export interface Claim {
  text: string;
  confidence: ConfidenceState;
  citations: Citation[];
}
export interface GraphHop {
  node: string | null;
  node_label: string | null;
  edge: string | null;
  detail: string | null;
}
export interface WhoToAsk {
  person: string;
  expertise: string;
  tenure_years: number | null;
}
export interface InvestigationResult {
  investigation_id: string;
  question: string;
  as_of: string | null;
  abstained: boolean;
  answer: string;
  claims: Claim[];
  graph_path: GraphHop[];
  unresolved: string[];
  who_to_ask: WhoToAsk[];
  degradation_level: string;
  prompt_manifest_hash: string | null;
  model_id: string | null;
  context_span_ids: string[];
}

export interface StreamEvent {
  type:
    | "banner"
    | "stage"
    | "token"
    | "claim"
    | "graph_hop"
    | "verdict"
    | "abstain"
    | "done"
    | "error";
  [k: string]: unknown;
}

export interface Me {
  subject: string;
  name: string;
  role: string;
  tenant: string;
  site: string;
  modules: string[];
}

/** One captured piece of expertise. `text` is the knowledge itself; `span_id` is present when
 *  it was written as a citable span, which is what lets it appear in an answer. */
export interface KnowledgeItem {
  target_kind: string;
  target_ref: string;
  label: string;
  text: string;
  kind: string; // tip | rule | faq | lesson | incident
  tags: string[];
  captured_on: string | null;
  span_id: string | null;
  used_in_answers: number;
}

export interface ExpertiseRecord {
  person_id: string;
  name: string;
  role: string;
  tenure_years: number;
  knows: KnowledgeItem[];
  retirement_risk: boolean;
}

export interface ResolutionProposal {
  proposal_id: string;
  canonical_asset_id: string;
  canonical_tag: string;
  identifier_ids: string[];
  identifiers: { id: string; value: string; source_system: string; vocabulary: string }[];
  score: number;
  method: string;
  features: Record<string, number>;
}

export interface ComplianceRow {
  clause: string;
  instrument: string;
  authority: string;
  asset_id: string;
  asset_tag: string;
  periodicity_months: number;
  last_evidence_date: string | null;
  last_evidence_doc: string | null;
  status: "satisfied" | "due" | "overdue" | "unknown";
}
export interface Coverage {
  encoded_clauses: number;
  total_applicable_clauses: number;
  by_instrument: Record<string, { encoded: number; total: number }>;
  disclaimer: string;
}

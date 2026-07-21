// The workspace: a persistent sidebar plus one main view.
//
// View switching is state-based, not routed — the URL stays "/" so the service-worker shell
// stays a single cached document and there is no history/offline edge case to manage.
// react-router is no longer a dependency of this app.
//
// The investigation controller lives HERE, above the views, so a run started in Ask keeps
// streaming while the user reads Alerts or the map and is still there when they come back.
import { useCallback, useEffect, useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { loadAlerts, type Alert } from "./lib/alerts";
import type { Coverage } from "./lib/types";
import { useInvestigation } from "./lib/useInvestigation";
import { viewById, type ViewId } from "./lib/views";
import { AlertsView } from "./views/AlertsView";
import { AskView } from "./views/AskView";
import { AssetMapView } from "./views/AssetMapView";
import { DocumentsView } from "./views/DocumentsView";
import { FieldModeView } from "./views/FieldModeView";
import { KnowledgeMapView } from "./views/KnowledgeMapView";
import { DecisionsView } from "./views/DecisionsView";
import { ExpertKnowledgeView } from "./views/ExpertKnowledgeView";
import { PastAnswersView } from "./views/PastAnswersView";
import { AuditView, CoverageView } from "./views/TrustViews";

export default function App() {
  const [view, setView] = useState<ViewId>("ask");
  const { run, ask } = useInvestigation();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [coverage, setCoverage] = useState<Coverage | null>(null);
  const [alertsLoading, setAlertsLoading] = useState(true);

  useEffect(() => {
    loadAlerts()
      .then((payload) => {
        setAlerts(payload.alerts);
        setCoverage(payload.coverage);
      })
      .catch(() => setAlerts([]))
      .finally(() => setAlertsLoading(false));
  }, []);

  // Jumping to Ask with a question runs it immediately; an empty string just focuses the view.
  const askAndGo = useCallback(
    (q: string) => {
      setView("ask");
      window.scrollTo({ top: 0, behavior: "smooth" });
      if (q.trim()) ask(q);
    },
    [ask],
  );

  const def = viewById(view);

  return (
    <div className="workspace">
      <Sidebar current={view} onSelect={setView} />

      <main
        style={{
          flex: 1,
          minWidth: 0,
          padding: "var(--sp-xl) var(--sp-lg) var(--sp-section)",
        }}
      >
        <div style={{ maxWidth: "var(--container)", margin: "0 auto" }}>
          {view === "ask" && (
            <AskView
              run={run}
              onAsk={ask}
              alerts={alerts}
              onOpenMap={() => setView("map")}
              onOpenAlerts={() => setView("alerts")}
            />
          )}
          {view === "past" && <PastAnswersView onAsk={askAndGo} />}
          {view === "documents" && <DocumentsView />}
          {view === "alerts" && (
            <AlertsView
              alerts={alerts}
              coverage={coverage}
              loading={alertsLoading}
              onAsk={askAndGo}
            />
          )}
          {view === "map" && <KnowledgeMapView run={run} onAskAbout={askAndGo} />}
          {view === "assets" && <AssetMapView alerts={alerts} onAsk={askAndGo} />}
          {view === "expert" && (
            <ExpertKnowledgeView onAsk={askAndGo} onOpenAlerts={() => setView("alerts")} />
          )}
          {view === "decisions" && <DecisionsView onAsk={askAndGo} />}
          {view === "audit" && <AuditView />}
          {view === "coverage" && <CoverageView coverage={coverage} />}
          {view === "field" && <FieldModeView run={run} onAsk={ask} />}

          {/* Screen-reader announcement of the current view. */}
          <span aria-live="polite" className="sr-only">
            {def.title}
          </span>
        </div>
      </main>
    </div>
  );
}

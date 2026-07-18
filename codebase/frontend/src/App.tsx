import { useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { Shell } from "./components/Shell";
import { useAuth } from "./lib/auth";
import { AssetMap } from "./pages/AssetMap";
import { Compliance } from "./pages/Compliance";
import { Execution } from "./pages/Execution";
import { FieldMode } from "./pages/FieldMode";
import { Home } from "./pages/Home";
import { Investigation } from "./pages/Investigation";
import { Login } from "./pages/Login";
import { Admin, Analytics, Audit, Knowledge, OrgMemory, Replay } from "./pages/Modules";

export default function App() {
  const { me, loading } = useAuth();
  // The current CP-9 rung, surfaced app-wide via the DegradedBanner (lifted here so any module
  // that streams an investigation can update it).
  const [rung, setRung] = useState("full");

  if (loading)
    return (
      <div style={{ display: "grid", placeItems: "center", height: "100vh" }}>
        <span className="t-label">SENTINEL — loading…</span>
      </div>
    );

  if (!me)
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );

  return (
    <Shell rung={rung}>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/investigate" element={<Investigation onRung={setRung} />} />
        <Route path="/assets" element={<AssetMap />} />
        <Route path="/compliance" element={<Compliance />} />
        <Route path="/execution" element={<Execution />} />
        <Route path="/replay" element={<Replay />} />
        <Route path="/org-memory" element={<OrgMemory />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/knowledge" element={<Knowledge />} />
        <Route path="/audit" element={<Audit />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/field" element={<FieldMode onRung={setRung} rung={rung} />} />
        <Route path="/login" element={<Navigate to="/home" replace />} />
        <Route path="*" element={<Navigate to="/home" replace />} />
      </Routes>
    </Shell>
  );
}

// Global Shell (PRB §2.1) — nav, degraded banner, confidence legend, profile. Nav uses
// decision-intelligence names (never the underlying tech, PRB §0.8). Items with no access are
// hidden entirely (invisibility, not a greyed-out tease).
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { ConfidenceLegend } from "./primitives";

interface NavItem {
  to: string;
  label: string;
  module: string;
  group: string;
}

// Product names, not engineering names (PRB §2.0 naming law). Grouped per design.md sidebar.
const NAV: NavItem[] = [
  { to: "/investigate", label: "Decision Investigation", module: "M1", group: "Investigations" },
  { to: "/assets", label: "Living Asset Map", module: "M2", group: "Investigations" },
  { to: "/replay", label: "Decision Memory & Replay", module: "M3", group: "Investigations" },
  { to: "/compliance", label: "Compliance Intelligence", module: "M6", group: "Operations" },
  { to: "/execution", label: "Execution Center", module: "M7", group: "Operations" },
  { to: "/analytics", label: "Decision Analytics", module: "M10", group: "Operations" },
  { to: "/org-memory", label: "Organizational Memory", module: "M5", group: "Knowledge" },
  { to: "/knowledge", label: "Knowledge Evolution", module: "M4", group: "Knowledge" },
  { to: "/audit", label: "Audit & Provenance", module: "M9", group: "Administration" },
  { to: "/admin", label: "Admin & Ingestion", module: "M11", group: "Administration" },
];
const GROUPS = ["Investigations", "Operations", "Knowledge", "Administration"];

export function Shell({ children, rung }: { children: React.ReactNode; rung: string }) {
  const { me, logout } = useAuth();
  const nav = useNavigate();
  const allowed = new Set(me?.modules ?? []);

  return (
    <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", height: "100vh" }}>
      {/* Sidebar — held at canvas level so chrome recedes and content elevates */}
      <aside
        style={{
          background: "var(--canvas)",
          borderRight: "1px solid var(--hairline)",
          padding: "var(--sp-lg) var(--sp-sm)",
          overflowY: "auto",
        }}
      >
        <NavLink to="/home" style={{ display: "block", padding: "0 var(--sp-sm) var(--sp-lg)", color: "var(--ink)" }}>
          <div className="t-title" style={{ letterSpacing: "0.04em" }}>
            Prahari
          </div>
          <div className="t-metadata">Decision Intelligence OS</div>
        </NavLink>
        <NavLink
          to="/home"
          style={({ isActive }) => ({
            display: "block", padding: "8px 12px", borderRadius: "var(--r-sm)", fontSize: 13,
            marginBottom: "var(--sp-md)",
            color: isActive ? "var(--ink)" : "var(--ink-muted)",
            background: isActive ? "var(--signal-wash)" : "transparent",
            borderLeft: isActive ? "2px solid var(--signal)" : "2px solid transparent",
          })}
        >
          ◈ Home
        </NavLink>
        {GROUPS.map((g) => {
          const items = NAV.filter((n) => n.group === g && allowed.has(n.module));
          if (!items.length) return null;
          return (
            <div key={g} style={{ marginBottom: "var(--sp-lg)" }}>
              <div className="t-label" style={{ color: "var(--ink-faint)", padding: "0 var(--sp-sm) var(--sp-xs)" }}>
                {g}
              </div>
              {items.map((n) => (
                <NavLink
                  key={n.to}
                  to={n.to}
                  style={({ isActive }) => ({
                    display: "block",
                    padding: "8px 12px",
                    borderRadius: "var(--r-sm)",
                    fontSize: 13,
                    color: isActive ? "var(--ink)" : "var(--ink-muted)",
                    background: isActive ? "var(--signal-wash)" : "transparent",
                    borderLeft: isActive ? "2px solid var(--signal)" : "2px solid transparent",
                    marginBottom: 2,
                  })}
                >
                  {n.label}
                </NavLink>
              ))}
            </div>
          );
        })}
        <NavLink
          to="/field"
          style={{ display: "block", padding: "8px 12px", fontSize: 13, color: "var(--ink-muted)" }}
        >
          ⏻ Field Mode
        </NavLink>
      </aside>

      {/* Main region */}
      <div style={{ display: "flex", flexDirection: "column", overflow: "hidden" }}>
        <header
          style={{
            height: 56,
            background: "var(--canvas)",
            borderBottom: "1px solid var(--hairline)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 var(--sp-xl)",
            flexShrink: 0,
          }}
        >
          <ConfidenceLegend />
          <div className="row center" style={{ gap: "var(--sp-md)" }}>
            <span className="t-body-sm ink-muted">
              {me?.name} · <span className="t-label">{me?.role}</span>
            </span>
            <button
              className="btn btn-tertiary"
              onClick={() => {
                logout();
                nav("/login");
              }}
            >
              Sign out
            </button>
          </div>
        </header>
        {rung && rung !== "full" && <DegradedBannerWrap rung={rung} />}
        <main style={{ flex: 1, overflowY: "auto", padding: "var(--sp-xl)" }}>{children}</main>
      </div>
    </div>
  );
}

import { DegradedBanner } from "./DegradedBanner";
function DegradedBannerWrap({ rung }: { rung: string }) {
  return <DegradedBanner rung={rung} />;
}

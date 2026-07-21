// Persistent left rail. Calm ink-on-canvas: hairline group separators, active item marked by
// ink weight plus a 2px ink bar — never by colour alone.
//
// BREAKPOINTS LIVE IN CSS, NOT JS. An earlier version derived "is this mobile / is this a
// narrow desktop" from matchMedia + resize + ResizeObserver in React state, and it desynced
// from the stylesheet whenever the viewport changed without firing an event the listener saw
// (embedded viewports, host-driven resizes). The result was a mobile header rendered on a
// 1280px desktop. Now both layouts are always in the DOM and CSS shows exactly one, so the two
// can never disagree. JS state holds only user intent: the drawer, and the manual rail toggle.
//
// No auth chrome anywhere: no sign-out, no role chip, no avatar.
import { useState } from "react";
import { FIELD_VIEW, GROUPS, VIEWS, type ViewId } from "../lib/views";

function Item({
  glyph,
  label,
  helper,
  active,
  onSelect,
}: {
  glyph: string;
  label: string;
  helper: string;
  active: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      type="button"
      className={`side-item${active ? " is-active" : ""}`}
      onClick={onSelect}
      aria-current={active ? "page" : undefined}
      // The helper is never rendered inline — every destination must be visible at a glance
      // without scrolling — but it stays available on hover and to assistive tech.
      aria-label={`${label} — ${helper}`}
      title={`${label} — ${helper}`}
    >
      <span aria-hidden="true" className="side-glyph">
        {glyph}
      </span>
      <span className="side-label">{label}</span>
    </button>
  );
}

function NavBody({
  current,
  onPick,
}: {
  current: ViewId;
  onPick: (v: ViewId) => void;
}) {
  return (
    <nav className="side-nav" aria-label="Main">
      {GROUPS.map((g) => {
        const items = VIEWS.filter((v) => v.group === g);
        if (!items.length) return null;
        return (
          <div key={g} className="side-group">
            <div className="side-group-label t-label">{g}</div>
            {items.map((v) => (
              <Item
                key={v.id}
                glyph={v.glyph}
                label={v.label}
                helper={v.helper}
                active={current === v.id}
                onSelect={() => onPick(v.id)}
              />
            ))}
          </div>
        );
      })}
      <Item
        glyph={FIELD_VIEW.glyph}
        label={FIELD_VIEW.label}
        helper={FIELD_VIEW.helper}
        active={current === "field"}
        onSelect={() => onPick("field")}
      />
    </nav>
  );
}

export function Sidebar({
  current,
  onSelect,
}: {
  current: ViewId;
  onSelect: (v: ViewId) => void;
}) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  // null = follow the stylesheet's automatic rail behaviour; true/false = user overrode it.
  const [railOverride, setRailOverride] = useState<boolean | null>(null);

  function pick(v: ViewId) {
    onSelect(v);
    setDrawerOpen(false);
  }

  const asideClass = [
    "sidebar",
    "side-desktop",
    railOverride === true ? "is-rail" : "",
    railOverride === false ? "is-wide" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <>
      {/* Desktop rail — CSS hides this below 768px. */}
      <aside className={asideClass}>
        <div className="side-brand">
          <span className="side-brand-name t-display-sm">Prahari</span>
          <span className="side-brand-short t-display-sm" aria-hidden="true">
            P
          </span>
          <span className="side-sub t-caption">Industrial knowledge intelligence</span>
        </div>

        <NavBody current={current} onPick={pick} />

        <button
          type="button"
          className="btn btn--text side-collapse"
          onClick={() => setRailOverride((v) => (v === true ? false : true))}
          aria-label={railOverride === true ? "Expand sidebar" : "Collapse sidebar"}
        >
          <span className="side-collapse-wide">« Collapse</span>
          <span className="side-collapse-narrow" aria-hidden="true">
            »
          </span>
        </button>
      </aside>

      {/* Mobile bar + drawer — CSS hides this at 768px and up. */}
      <header className="side-mobile">
        <div className="side-mobile-bar">
          <span className="t-display-sm" style={{ fontSize: 22 }}>
            Prahari
          </span>
          <button
            type="button"
            className="btn btn--outline"
            aria-label={drawerOpen ? "Close menu" : "Open menu"}
            aria-expanded={drawerOpen}
            onClick={() => setDrawerOpen((v) => !v)}
            style={{ padding: "9px 14px" }}
          >
            {drawerOpen ? "✕" : "☰"}
          </button>
        </div>
        {drawerOpen && (
          <div className="side-drawer">
            <NavBody current={current} onPick={pick} />
          </div>
        )}
      </header>
    </>
  );
}

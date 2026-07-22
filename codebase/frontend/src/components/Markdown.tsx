// A small, safe Markdown renderer — enough for the industrial corpus (headings, tables, lists,
// blockquotes, rules, bold/italic/code). It renders to React nodes, never to raw HTML, so
// document text can never inject markup. Deliberately compact, not a full CommonMark engine.
import type { ReactNode } from "react";

/** Inline: **bold**, *italic*, `code`. Split on the markers and wrap the matched runs. */
function inline(text: string, keyBase: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g;
  let last = 0;
  let m: RegExpExecArray | null;
  let i = 0;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) nodes.push(text.slice(last, m.index));
    const tok = m[0];
    const key = `${keyBase}-${i++}`;
    if (tok.startsWith("**")) nodes.push(<strong key={key}>{tok.slice(2, -2)}</strong>);
    else if (tok.startsWith("`"))
      nodes.push(
        <code
          key={key}
          style={{
            font: "var(--t-body-sm)",
            fontFamily: "ui-monospace, monospace",
            background: "var(--surface-strong)",
            padding: "1px 5px",
            borderRadius: "var(--r-xs)",
          }}
        >
          {tok.slice(1, -1)}
        </code>,
      );
    else nodes.push(<em key={key}>{tok.slice(1, -1)}</em>);
    last = m.index + tok.length;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes;
}

function splitRow(line: string): string[] {
  return line
    .replace(/^\||\|$/g, "")
    .split("|")
    .map((c) => c.trim());
}
const isTableSep = (l: string) => /^\|?[\s:-]*-[\s:|-]*\|?$/.test(l) && l.includes("-");

export function Markdown({ text }: { text: string }) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const blocks: ReactNode[] = [];
  let i = 0;
  let key = 0;
  const K = () => `md-${key++}`;

  const hstyle = (lvl: number) =>
    ({
      1: { font: "var(--t-display-md)", margin: "var(--sp-lg) 0 var(--sp-sm)" },
      2: { font: "var(--t-display-sm)", margin: "var(--sp-lg) 0 var(--sp-xs)" },
      3: { font: "var(--t-title-md)", margin: "var(--sp-base) 0 var(--sp-xxs)", color: "var(--ink)" },
    }[Math.min(lvl, 3)] as React.CSSProperties);

  while (i < lines.length) {
    const line = lines[i];

    if (!line.trim()) {
      i++;
      continue;
    }

    // Heading
    const h = /^(#{1,6})\s+(.*)$/.exec(line);
    if (h) {
      const lvl = h[1].length;
      const Tag = (`h${Math.min(lvl + 1, 6)}` as unknown) as keyof JSX.IntrinsicElements;
      blocks.push(
        <Tag key={K()} className={lvl <= 2 ? "" : "t-title-sm"} style={hstyle(lvl)}>
          {inline(h[2], K())}
        </Tag>,
      );
      i++;
      continue;
    }

    // Horizontal rule
    if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      blocks.push(<hr key={K()} style={{ border: 0, borderTop: "1px solid var(--hairline)", margin: "var(--sp-base) 0" }} />);
      i++;
      continue;
    }

    // Table: a header row of pipes, then a separator row.
    if (line.includes("|") && i + 1 < lines.length && isTableSep(lines[i + 1])) {
      const header = splitRow(line);
      i += 2;
      const rows: string[][] = [];
      while (i < lines.length && lines[i].includes("|") && lines[i].trim()) {
        rows.push(splitRow(lines[i]));
        i++;
      }
      blocks.push(
        <div key={K()} style={{ overflowX: "auto", margin: "var(--sp-sm) 0" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 420 }}>
            <thead>
              <tr>
                {header.map((c, j) => (
                  <th
                    key={j}
                    style={{
                      textAlign: "left",
                      padding: "6px 10px",
                      borderBottom: "1px solid var(--hairline-strong)",
                      font: "var(--t-label)",
                      letterSpacing: "var(--ls-label)",
                      textTransform: "uppercase",
                      color: "var(--muted)",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {inline(c, K())}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, ri) => (
                <tr key={ri}>
                  {header.map((_, ci) => (
                    <td
                      key={ci}
                      className="t-body-sm"
                      style={{ padding: "6px 10px", borderBottom: "1px solid var(--hairline)", verticalAlign: "top" }}
                    >
                      {inline(r[ci] ?? "", K())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>,
      );
      continue;
    }

    // Blockquote
    if (/^>\s?/.test(line)) {
      const quote: string[] = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        quote.push(lines[i].replace(/^>\s?/, ""));
        i++;
      }
      blocks.push(
        <blockquote
          key={K()}
          style={{
            margin: "var(--sp-sm) 0",
            padding: "var(--sp-xs) var(--sp-base)",
            borderLeft: "3px solid var(--hairline-strong)",
            color: "var(--body)",
          }}
        >
          {inline(quote.join(" "), K())}
        </blockquote>,
      );
      continue;
    }

    // Unordered / ordered list
    const ul = /^\s*[-*+]\s+/.test(line);
    const ol = /^\s*\d+\.\s+/.test(line);
    if (ul || ol) {
      const items: string[] = [];
      const test = ul ? /^\s*[-*+]\s+/ : /^\s*\d+\.\s+/;
      while (i < lines.length && test.test(lines[i])) {
        items.push(lines[i].replace(test, ""));
        i++;
      }
      const ListTag = ol ? "ol" : "ul";
      blocks.push(
        <ListTag key={K()} style={{ margin: "var(--sp-xs) 0", paddingLeft: "var(--sp-lg)" }}>
          {items.map((it, j) => (
            <li key={j} className="t-body" style={{ marginBottom: 2 }}>
              {inline(it, K())}
            </li>
          ))}
        </ListTag>,
      );
      continue;
    }

    // Paragraph — gather until blank line.
    const para: string[] = [];
    while (i < lines.length && lines[i].trim() && !/^(#{1,6}\s|>\s?|\s*[-*+]\s|\s*\d+\.\s)/.test(lines[i])) {
      if (lines[i].includes("|") && i + 1 < lines.length && isTableSep(lines[i + 1])) break;
      para.push(lines[i]);
      i++;
    }
    if (para.length) {
      blocks.push(
        <p key={K()} className="t-body" style={{ margin: "var(--sp-xs) 0", lineHeight: 1.6 }}>
          {inline(para.join(" "), K())}
        </p>,
      );
    }
  }

  return <div>{blocks}</div>;
}

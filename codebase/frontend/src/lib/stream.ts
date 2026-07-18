// WebSocket streaming client for a live investigation (Bible §7.4).
// Renders the traversal as it happens (Vol 1 §1.8: show the traversal, not just the answer).
import { getToken } from "./api";
import type { StreamEvent } from "./types";

export function streamInvestigation(
  investigationId: string,
  onEvent: (ev: StreamEvent) => void,
  onClose?: () => void,
): () => void {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const token = getToken() ?? "";
  const url = `${proto}://${location.host}/v1/stream/investigations/${investigationId}?token=${encodeURIComponent(
    token,
  )}`;
  const ws = new WebSocket(url);
  ws.onmessage = (msg) => {
    try {
      onEvent(JSON.parse(msg.data) as StreamEvent);
    } catch {
      /* ignore malformed frame */
    }
  };
  ws.onclose = () => onClose?.();
  ws.onerror = () => onClose?.();
  return () => ws.close();
}

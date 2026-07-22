// A tiny event bus so any "Ask about this" affordance, anywhere in the app, can open the
// floating chat widget with context — without threading a prop through every view or
// navigating away from the current page.
export interface ChatOpenDetail {
  /** The question to ask. Empty just opens the widget without running anything. */
  prompt: string;
  /** A short label for what this ask is about (asset tag, alert title, item name). Shown as a
   *  chip at the top of the panel so the user sees the context that seeded the question. */
  context?: string;
}

const EVENT = "prahari:open-chat";

export function openChat(detail: ChatOpenDetail): void {
  window.dispatchEvent(new CustomEvent<ChatOpenDetail>(EVENT, { detail }));
}

export function onOpenChat(cb: (detail: ChatOpenDetail) => void): () => void {
  const handler = (e: Event) => cb((e as CustomEvent<ChatOpenDetail>).detail);
  window.addEventListener(EVENT, handler);
  return () => window.removeEventListener(EVENT, handler);
}

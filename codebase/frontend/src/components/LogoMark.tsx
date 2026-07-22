// The Prahari mark — a double-infinity knot, drawn inline so it is truly transparent and takes
// its colour from `currentColor` (ink on light surfaces, white on dark). No background plate.
export function LogoMark({ width = 34 }: { width?: number }) {
  const height = Math.round((width * 44) / 96);
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 96 44"
      fill="none"
      aria-hidden="true"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M36 22 C28 7 16 7 16 22 C16 37 28 37 36 22 C44 7 56 7 56 22 C56 37 44 37 36 22 Z"
        stroke="currentColor"
        strokeWidth={6}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M60 22 C52 7 40 7 40 22 C40 37 52 37 60 22 C68 7 80 7 80 22 C80 37 68 37 60 22 Z"
        stroke="currentColor"
        strokeWidth={6}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

type IconName = "calendar" | "building" | "check" | "alert" | "shield" | "clock" | "spark" | "info" | "video" | "document";
const paths: Record<IconName, string> = {
  calendar: "M8 2v4m8-4v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14H3V6a2 2 0 0 1 2-2Zm2 10h3m4 0h3m-10 4h3",
  building: "M4 21V5l8-3 8 3v16M2 21h20M8 7h1m6 0h1M8 11h1m6 0h1M8 15h1m6 0h1m-6 6v-4h4v4",
  check: "m7 12 3 3 7-7M21 12a9 9 0 1 1-5-8",
  alert: "m10.3 3.9-8.1 14a2 2 0 0 0 1.7 3h16.2a2 2 0 0 0 1.7-3l-8.1-14a2 2 0 0 0-3.4 0ZM12 9v4m0 4h.01",
  shield: "m12 2 8 4v6c0 5-8 10-8 10S4 17 4 12V6l8-4Zm-4 10 3 3 5-6",
  clock: "M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-5v5l3 2",
  spark: "m12 3 2.7 6.3L21 12l-6.3 2.7L12 21l-2.7-6.3L3 12l6.3-2.7L12 3Zm7-2v4m-2-2h4",
  info: "M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-1v6m0-10h.01",
  video: "M3 5h12v14H3V5Zm12 5 6-4v12l-6-4",
  document: "M14 2H4v20h16V8l-6-6Zm0 0v6h6M8 12h8m-8 4h6",
};
export function Icon({ name }: { name: IconName }) {
  return <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.65" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={paths[name]} /></svg>;
}

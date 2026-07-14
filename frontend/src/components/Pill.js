import React from "react";

export default function Pill({ status }) {
  const cls = "pill pill-" + (status || "").toLowerCase();
  return <span className={cls}>{status}</span>;
}

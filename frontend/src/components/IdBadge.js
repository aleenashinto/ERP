import React from "react";

function initials(name) {
  if (!name) return "?";
  const parts = name.trim().split(" ");
  return (parts[0]?.[0] || "") + (parts[1]?.[0] || "");
}

export default function IdBadge({ name, meta }) {
  return (
    <span className="id-badge">
      <span className="avatar">{initials(name).toUpperCase()}</span>
      <span>
        <div className="name">{name || "Unknown"}</div>
        {meta && <div className="meta">{meta}</div>}
      </span>
    </span>
  );
}

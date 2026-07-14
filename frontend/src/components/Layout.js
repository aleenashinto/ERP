import React from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/employees", label: "Employees" },
  { to: "/departments", label: "Departments" },
  { to: "/attendance", label: "Attendance" },
  { to: "/leaves", label: "Leaves" },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-logo"><span className="dot" />Office ERP</div>
        <nav>
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          Signed in as<br /><strong style={{ color: "#fff" }}>{user?.full_name || user?.username}</strong><br />
          {user?.role}
        </div>
      </aside>
      <div className="main-area">
        <header className="topbar">
          <div className="muted" style={{ fontSize: 13 }}>Office ERP System</div>
          <button className="btn btn-ghost btn-sm" onClick={logout}>Log out</button>
        </header>
        <main className="page-content">{children}</main>
      </div>
    </div>
  );
}

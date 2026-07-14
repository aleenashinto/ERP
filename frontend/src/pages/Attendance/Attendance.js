import React, { useEffect, useState } from "react";
import api from "../../services/api";
import IdBadge from "../../components/IdBadge";
import Pill from "../../components/Pill";
import { useAuth } from "../../context/AuthContext";

export default function Attendance() {
  const { hasRole } = useAuth();
  const isManager = hasRole("HR", "MANAGER", "TEAM_LEAD", "SUPER_ADMIN");
  const [records, setRecords] = useState([]);
  const [today, setToday] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionError, setActionError] = useState("");

  const load = () => {
    setLoading(true);
    const now = new Date();
    api
      .get("/attendance/monthly/", { params: { year: now.getFullYear(), month: now.getMonth() + 1 } })
      .then((res) => {
        setRecords(res.data);
        const todayStr = now.toISOString().slice(0, 10);
        setToday(res.data.find((r) => r.date === todayStr) || null);
      })
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const checkIn = async () => {
    setActionError("");
    try {
      await api.post("/attendance/check_in/");
      load();
    } catch (err) {
      setActionError(err.response?.data?.detail || "Could not check in.");
    }
  };

  const checkOut = async () => {
    setActionError("");
    try {
      await api.post("/attendance/check_out/");
      load();
    } catch (err) {
      setActionError(err.response?.data?.detail || "Could not check out.");
    }
  };

  return (
    <div>
      <h2>Attendance</h2>
      <p className="muted" style={{ marginBottom: 18 }}>
        {isManager ? "Attendance across the team for this month." : "Your check-ins for this month."}
      </p>

      {!isManager && (
        <div className="card" style={{ marginBottom: 16, display: "flex", gap: 12, alignItems: "center" }}>
          <button className="btn btn-primary" onClick={checkIn} disabled={!!today?.check_in}>
            {today?.check_in ? `Checked in at ${today.check_in}` : "Check In"}
          </button>
          <button className="btn btn-ghost" onClick={checkOut} disabled={!today?.check_in || !!today?.check_out}>
            {today?.check_out ? `Checked out at ${today.check_out}` : "Check Out"}
          </button>
          {actionError && <span className="error-text">{actionError}</span>}
        </div>
      )}

      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              {isManager && <th>Employee</th>}
              <th>Date</th>
              <th>Check In</th>
              <th>Check Out</th>
              <th>Hours</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {loading && <tr><td colSpan={6} className="muted" style={{ padding: 20 }}>Loading...</td></tr>}
            {!loading && records.length === 0 && (
              <tr><td colSpan={6} className="muted" style={{ padding: 20 }}>No attendance records yet this month.</td></tr>
            )}
            {records.map((r) => (
              <tr key={r.id}>
                {isManager && <td><IdBadge name={r.employee_name} /></td>}
                <td>{r.date}</td>
                <td>{r.check_in || "—"}</td>
                <td>{r.check_out || "—"}</td>
                <td>{r.hours_worked ?? "—"}</td>
                <td>{r.is_late ? <Pill status="Late" /> : <Pill status="Active" />}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

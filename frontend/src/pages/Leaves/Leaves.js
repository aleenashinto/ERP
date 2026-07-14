import React, { useEffect, useState } from "react";
import api from "../../services/api";
import IdBadge from "../../components/IdBadge";
import Pill from "../../components/Pill";
import { useAuth } from "../../context/AuthContext";

const LEAVE_TYPES = [
  { value: "CASUAL", label: "Casual Leave" },
  { value: "SICK", label: "Sick Leave" },
  { value: "PAID", label: "Paid Leave" },
  { value: "WFH", label: "Work From Home" },
];

export default function Leaves() {
  const { hasRole } = useAuth();
  const isManager = hasRole("HR", "MANAGER", "TEAM_LEAD", "SUPER_ADMIN");
  const [leaves, setLeaves] = useState([]);
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ leave_type: "CASUAL", start_date: "", end_date: "", reason: "" });
  const [error, setError] = useState("");

  const load = () => {
    setLoading(true);
    api.get("/leaves/").then((res) => setLeaves(res.data.results ?? res.data)).finally(() => setLoading(false));
    if (!isManager) {
      api.get("/leaves/balance/mine/").then((res) => setBalance(res.data));
    }
  };

  useEffect(load, []); // eslint-disable-line react-hooks/exhaustive-deps

  const submitLeave = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.post("/leaves/", form);
      setForm({ leave_type: "CASUAL", start_date: "", end_date: "", reason: "" });
      load();
    } catch (err) {
      setError(err.response?.data?.non_field_errors?.[0] || "Could not submit leave request.");
    }
  };

  const cancel = async (id) => {
    await api.post(`/leaves/${id}/cancel/`);
    load();
  };

  const decide = async (id, action) => {
    await api.post(`/leaves/${id}/${action}/`);
    load();
  };

  return (
    <div>
      <h2>Leave Management</h2>
      <p className="muted" style={{ marginBottom: 18 }}>
        {isManager ? "Review and decide on leave requests." : "Apply for leave and track your requests."}
      </p>

      {!isManager && (
        <div className="grid-2" style={{ marginBottom: 16 }}>
          <form className="card" onSubmit={submitLeave}>
            <div className="section-title">Apply for Leave</div>
            <div className="field">
              <label>Leave type</label>
              <select value={form.leave_type} onChange={(e) => setForm({ ...form, leave_type: e.target.value })}>
                {LEAVE_TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
              </select>
            </div>
            <div style={{ display: "flex", gap: 10 }}>
              <div className="field" style={{ flex: 1 }}>
                <label>Start date</label>
                <input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} required />
              </div>
              <div className="field" style={{ flex: 1 }}>
                <label>End date</label>
                <input type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} required />
              </div>
            </div>
            <div className="field">
              <label>Reason</label>
              <textarea rows={2} value={form.reason} onChange={(e) => setForm({ ...form, reason: e.target.value })} />
            </div>
            {error && <div className="error-text" style={{ marginBottom: 10 }}>{error}</div>}
            <button className="btn btn-primary">Submit Request</button>
          </form>

          {balance && (
            <div className="card">
              <div className="section-title">Leave Balance</div>
              <div className="stat-grid" style={{ gridTemplateColumns: "1fr", gap: 10 }}>
                <div className="flex-between"><span className="muted">Casual Leave</span><strong>{balance.casual_leave} days</strong></div>
                <div className="flex-between"><span className="muted">Sick Leave</span><strong>{balance.sick_leave} days</strong></div>
                <div className="flex-between"><span className="muted">Paid Leave</span><strong>{balance.paid_leave} days</strong></div>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              {isManager && <th>Employee</th>}
              <th>Type</th>
              <th>Dates</th>
              <th>Days</th>
              <th>Reason</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {loading && <tr><td colSpan={7} className="muted" style={{ padding: 20 }}>Loading...</td></tr>}
            {!loading && leaves.length === 0 && (
              <tr><td colSpan={7} className="muted" style={{ padding: 20 }}>No leave requests found.</td></tr>
            )}
            {leaves.map((l) => (
              <tr key={l.id}>
                {isManager && <td><IdBadge name={l.employee_name} /></td>}
                <td>{LEAVE_TYPES.find((t) => t.value === l.leave_type)?.label || l.leave_type}</td>
                <td>{l.start_date} → {l.end_date}</td>
                <td>{l.days_requested}</td>
                <td className="muted">{l.reason || "—"}</td>
                <td><Pill status={l.status.charAt(0) + l.status.slice(1).toLowerCase()} /></td>
                <td>
                  {!isManager && l.status === "PENDING" && (
                    <button className="btn btn-ghost btn-sm" onClick={() => cancel(l.id)}>Cancel</button>
                  )}
                  {isManager && l.status === "PENDING" && (
                    <div style={{ display: "flex", gap: 6 }}>
                      <button className="btn btn-primary btn-sm" onClick={() => decide(l.id, "approve")}>Approve</button>
                      <button className="btn btn-danger btn-sm" onClick={() => decide(l.id, "reject")}>Reject</button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

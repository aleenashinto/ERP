import React, { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import api from "../../services/api";
import IdBadge from "../../components/IdBadge";

const COLORS = ["#E8A33D", "#5C8A66", "#1C2430", "#D9634C", "#8B92A3"];

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/dashboard/summary/").then((res) => setSummary(res.data)).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="muted">Loading dashboard...</div>;
  if (!summary) return <div className="muted">Couldn't load dashboard data.</div>;

  const leaveData = [
    { name: "Pending", value: summary.leave_statistics.pending },
    { name: "Approved", value: summary.leave_statistics.approved },
    { name: "Rejected", value: summary.leave_statistics.rejected },
  ];

  return (
    <div>
      <h2>Dashboard</h2>
      <p className="muted" style={{ marginBottom: 20 }}>A snapshot of today's office activity.</p>

      <div className="stat-grid">
        <div className="card stat-card">
          <div className="label">Total Employees</div>
          <div className="value">{summary.total_employees}</div>
        </div>
        <div className="card stat-card">
          <div className="label">Checked In Today</div>
          <div className="value">{summary.today_attendance}</div>
        </div>
        <div className="card stat-card">
          <div className="label">Pending Leaves</div>
          <div className="value">{summary.pending_leaves}</div>
        </div>
        <div className="card stat-card">
          <div className="label">Departments</div>
          <div className="value">{summary.department_distribution.length}</div>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="section-title">Department Distribution</div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={summary.department_distribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E4E4E0" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="count" fill="#E8A33D" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="section-title">Leave Statistics</div>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={leaveData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={80} paddingAngle={3}>
                {leaveData.map((entry, i) => (
                  <Cell key={entry.name} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card mt-16">
        <div className="section-title">Upcoming Birthdays (next 7 days)</div>
        {summary.upcoming_birthdays.length === 0 ? (
          <div className="muted">No birthdays coming up this week.</div>
        ) : (
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {summary.upcoming_birthdays.map((b) => (
              <IdBadge key={b.name + b.date} name={b.name} meta={b.date} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

import React, { useEffect, useState } from "react";
import api from "../../services/api";
import IdBadge from "../../components/IdBadge";
import Pill from "../../components/Pill";

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    const params = {};
    if (search) params.search = search;
    if (statusFilter) params.status = statusFilter;
    api.get("/employees/", { params }).then((res) => setEmployees(res.data.results ?? res.data)).finally(() => setLoading(false));
  };

  useEffect(() => {
    const timeout = setTimeout(load, 300); // debounce search-as-you-type
    return () => clearTimeout(timeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search, statusFilter]);

  return (
    <div>
      <div className="flex-between">
        <h2>Employee Directory</h2>
      </div>
      <p className="muted" style={{ marginBottom: 18 }}>Search and filter across the whole organization.</p>

      <div className="card" style={{ marginBottom: 16, display: "flex", gap: 12 }}>
        <div style={{ flex: 1 }}>
          <input placeholder="Search by name, ID, or designation..." value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        <div style={{ width: 180 }}>
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="">All statuses</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
      </div>

      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>Employee</th>
              <th>Employee ID</th>
              <th>Department</th>
              <th>Designation</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr><td colSpan={5} className="muted" style={{ padding: 20 }}>Loading...</td></tr>
            )}
            {!loading && employees.length === 0 && (
              <tr><td colSpan={5} className="muted" style={{ padding: 20 }}>No employees match your filters.</td></tr>
            )}
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td><IdBadge name={emp.user.full_name} meta={emp.user.email} /></td>
                <td>{emp.employee_id}</td>
                <td>{emp.department_name || "—"}</td>
                <td>{emp.designation || "—"}</td>
                <td><Pill status={emp.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

import React, { useEffect, useState } from "react";
import api from "../../services/api";
import { useAuth } from "../../context/AuthContext";

export default function Departments() {
  const { hasRole } = useAuth();
  const canManage = hasRole("HR", "SUPER_ADMIN");
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = () => {
    setLoading(true);
    api.get("/departments/").then((res) => setDepartments(res.data.results ?? res.data)).finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.post("/departments/", { name, description });
      setName("");
      setDescription("");
      load();
    } catch (err) {
      setError(err.response?.data?.name?.[0] || "Could not add department.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this department?")) return;
    await api.delete(`/departments/${id}/`);
    load();
  };

  return (
    <div>
      <h2>Departments</h2>
      <p className="muted" style={{ marginBottom: 18 }}>Organize employees into departments and track headcount.</p>

      {canManage && (
        <form className="card" style={{ marginBottom: 16, display: "flex", gap: 12, alignItems: "flex-end" }} onSubmit={handleAdd}>
          <div className="field" style={{ flex: 1, marginBottom: 0 }}>
            <label>Department name</label>
            <input value={name} onChange={(e) => setName(e.target.value)} required />
          </div>
          <div className="field" style={{ flex: 2, marginBottom: 0 }}>
            <label>Description</label>
            <input value={description} onChange={(e) => setDescription(e.target.value)} />
          </div>
          <button className="btn btn-primary">Add Department</button>
        </form>
      )}
      {error && <div className="error-text mt-16">{error}</div>}

      <div className="card" style={{ padding: 0, marginTop: 16 }}>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Head</th>
              <th>Employees</th>
              {canManage && <th></th>}
            </tr>
          </thead>
          <tbody>
            {loading && <tr><td colSpan={5} className="muted" style={{ padding: 20 }}>Loading...</td></tr>}
            {!loading && departments.map((d) => (
              <tr key={d.id}>
                <td><strong>{d.name}</strong></td>
                <td className="muted">{d.description || "—"}</td>
                <td>{d.head_name || "—"}</td>
                <td>{d.employee_count}</td>
                {canManage && (
                  <td>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(d.id)}>Delete</button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

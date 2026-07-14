import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate("/");
    } catch (err) {
      setError("Invalid username or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div className="login-logo"><span style={{ width: 10, height: 10, borderRadius: 2, background: "#E8A33D", display: "inline-block" }} />Office ERP</div>
        <div className="login-sub">Sign in to your workspace</div>
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Username</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} required autoFocus />
          </div>
          <div className="field">
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          {error && <div className="error-text">{error}</div>}
          <button className="btn btn-primary" style={{ width: "100%", justifyContent: "center", marginTop: 6 }} disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>
        <div className="hint-text">
          Demo accounts (after running <code>seed_demo_data</code>):<br />
          admin / Admin@12345 &nbsp;·&nbsp; hr_jane / Hr@12345 &nbsp;·&nbsp; john_dev / John@12345
        </div>
      </div>
    </div>
  );
}

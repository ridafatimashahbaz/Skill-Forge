import { useState, FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import { useAuth } from "../context/AuthContext";

export function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    try {
      const res = await api.login({ email, password });
      login(res.access_token, res.role, res.user_id);
      navigate(res.role === "student" ? "/dashboard" : "/mentor");
    } catch (err: any) {
      setError(err.message);
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-24 px-6">
      <h2 className="text-2xl font-display font-semibold mb-6">Log in</h2>
      <form onSubmit={onSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border border-ink/20 rounded-lg px-3 py-2"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border border-ink/20 rounded-lg px-3 py-2"
          required
        />
        {error && <p className="text-ember text-sm">{error}</p>}
        <button className="w-full bg-forge text-white rounded-lg py-2 font-medium hover:bg-forge-dark">
          Log in
        </button>
      </form>
      <p className="text-sm text-ink/60 mt-4">
        No account? <Link to="/signup" className="text-forge">Sign up</Link>
      </p>
    </div>
  );
}

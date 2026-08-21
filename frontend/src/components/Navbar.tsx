import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function Navbar() {
  const { role, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="border-b border-ink/10 bg-paper">
      <div className="max-w-5xl mx-auto flex items-center justify-between px-6 py-4">
        <div className="flex items-baseline gap-2">
          <h1 className="text-lg font-display font-semibold text-ink">SkillForge</h1>
          {role && <span className="text-xs uppercase tracking-wide text-forge">{role}</span>}
        </div>
        {role && (
          <button
            onClick={() => {
              logout();
              navigate("/login");
            }}
            className="text-sm text-ink/60 hover:text-ember"
          >
            Sign out
          </button>
        )}
      </div>
    </header>
  );
}

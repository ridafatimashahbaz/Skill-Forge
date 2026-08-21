import { createContext, useContext, useState, ReactNode } from "react";

type AuthState = {
  token: string | null;
  role: string | null;
  userId: string | null;
  login: (token: string, role: string, userId: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem("sf_token"));
  const [role, setRole] = useState<string | null>(localStorage.getItem("sf_role"));
  const [userId, setUserId] = useState<string | null>(localStorage.getItem("sf_user_id"));

  const login = (t: string, r: string, uid: string) => {
    localStorage.setItem("sf_token", t);
    localStorage.setItem("sf_role", r);
    localStorage.setItem("sf_user_id", uid);
    setToken(t);
    setRole(r);
    setUserId(uid);
  };

  const logout = () => {
    localStorage.removeItem("sf_token");
    localStorage.removeItem("sf_role");
    localStorage.removeItem("sf_user_id");
    setToken(null);
    setRole(null);
    setUserId(null);
  };

  return (
    <AuthContext.Provider value={{ token, role, userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}

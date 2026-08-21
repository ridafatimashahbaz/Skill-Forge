import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { Navbar } from "./components/Navbar";
import { Login } from "./pages/Login";
import { Signup } from "./pages/Signup";
import { StudentDashboard } from "./pages/StudentDashboard";
import { MentorDashboard } from "./pages/MentorDashboard";

function Protected({ children, roles }: { children: JSX.Element; roles?: string[] }) {
  const { token, role } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  if (roles && role && !roles.includes(role)) return <Navigate to="/login" replace />;
  return children;
}

function Shell() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/dashboard"
          element={
            <Protected roles={["student"]}>
              <StudentDashboard />
            </Protected>
          }
        />
        <Route
          path="/mentor"
          element={
            <Protected roles={["mentor", "admin"]}>
              <MentorDashboard />
            </Protected>
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  );
}

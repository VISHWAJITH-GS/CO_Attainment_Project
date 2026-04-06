import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import { Navigate, Outlet, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { Navbar } from "./components/layout/Navbar";
import { Sidebar } from "./components/layout/Sidebar";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import SubjectWorkspace from "./pages/SubjectWorkspace";

/** Wraps the nested Outlet with AnimatePresence keyed on location */
function AnimatedOutlet() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait" initial={false}>
      {/* Outlet is re-mounted when the key (pathname) changes */}
      <Outlet key={location.pathname} />
    </AnimatePresence>
  );
}

function DashboardLayout({ user, onLogout }) {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar
        user={user}
        onMenuClick={() => setSidebarOpen(true)}
        onOpenProfile={() => navigate("/profile")}
        onOpenSettings={() => navigate("/settings")}
        onLogout={onLogout}
      />

      <div className="pt-24 md:pt-20">
        <Sidebar
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          collapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed((prev) => !prev)}
        />

        <main
          className={
            `h-[calc(100vh-6rem)] md:h-[calc(100vh-5rem)] min-w-0 overflow-y-auto transition-[margin] duration-300 ${
              sidebarCollapsed ? "md:ml-[70px]" : "md:ml-[240px]"
            }`
          }
        >
          {/* AnimatedOutlet handles page transitions within the dashboard shell */}
          <AnimatedOutlet />
        </main>
      </div>
    </div>
  );
}

function App() {
  const [currentUser, setCurrentUser] = useState(null);

  return (
    <Routes>
      <Route path="/" element={<Navigate to={currentUser ? "/dashboard" : "/login"} replace />} />
      <Route path="/login" element={<Login onLogin={setCurrentUser} />} />
      <Route
        element={
          <DashboardLayout
            user={currentUser}
            onLogout={() => setCurrentUser(null)}
          />
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/subjects" element={<SubjectWorkspace />} />
        <Route path="/subjects/:subjectCode/workspace" element={<SubjectWorkspace />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default App;
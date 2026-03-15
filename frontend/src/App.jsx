import { useState } from "react";
import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import { Navbar } from "./components/layout/Navbar";
import { Sidebar } from "./components/layout/Sidebar";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Subjects from "./pages/Subjects";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";

function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar
        onMenuClick={() => setSidebarOpen(true)}
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
          <Outlet />
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/login" element={<Login />} />
      <Route element={<DashboardLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/subjects" element={<Subjects />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default App;
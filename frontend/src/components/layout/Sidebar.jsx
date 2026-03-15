import { Home, BookOpen, BarChart3, Settings, ChevronsLeft, ChevronsRight, LogOut, X } from "lucide-react";
import { Button } from "../ui/button";
import { cn } from "../../lib/utils";
import { SidebarItem } from "./SidebarItem";

const navItems = [
  { label: "Dashboard", icon: Home, to: "/dashboard" },
  { label: "My Subjects", icon: BookOpen, to: "/subjects" },
  { label: "Reports", icon: BarChart3, to: "/reports" },
  { label: "Settings", icon: Settings, to: "/settings" },
];

function SidebarContent({ collapsed = false, onClose, onToggleCollapse, desktop = false }) {
  return (
    <div className="flex h-full flex-col bg-white">
      <div className={cn("group border-b border-red-100 px-4 py-3", collapsed && "px-2")}>
        {collapsed ? (
          <div className="flex items-center justify-between gap-2">
            <img src="/tce-logov2.png" alt="TCE ICON" className="h-9 w-auto" />
            {desktop && (
              <Button variant="ghost" className="h-8 w-8 p-0" onClick={onToggleCollapse} aria-label="Expand sidebar">
                <ChevronsRight size={16} />
              </Button>
            )}
          </div>
        ) : (
          <div className="flex items-center justify-between gap-2">
            <div className="min-w-0">
              <img src="/tce-logov2.png" alt="TCE ICON" className="h-12 w-auto" />
              <p className="mt-1 truncate text-xs font-semibold uppercase tracking-[0.18em] text-red-700/80">TCE COAS</p>
            </div>
            {desktop && (
              <Button
                variant="ghost"
                className="h-8 w-8 shrink-0 p-0 opacity-0 transition-opacity group-hover:opacity-100 focus-visible:opacity-100"
                onClick={onToggleCollapse}
                aria-label="Collapse sidebar"
              >
                <ChevronsLeft size={16} />
              </Button>
            )}
          </div>
        )}
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-3">
        {navItems.map((item) => {
          return (
            <SidebarItem
              key={item.label}
              to={item.to}
              icon={item.icon}
              label={item.label}
              collapsed={collapsed}
              onNavigate={onClose}
            />
          );
        })}
      </nav>

      <div className="border-t border-red-100 p-3">
        <Button
          variant="ghost"
          className={cn("w-full text-slate-700 hover:text-red-900", collapsed ? "justify-center px-0" : "justify-start gap-2")}
          title={collapsed ? "Sign out" : undefined}
          onClick={onClose}
        >
          <LogOut size={16} />
          {!collapsed && "Sign out"}
        </Button>
      </div>
    </div>
  );
}

export function Sidebar({ open, onClose, collapsed = false, onToggleCollapse }) {
  return (
    <>
      <aside
        className={cn(
          "fixed bottom-0 left-0 top-24 z-30 hidden border-r border-red-100 bg-white transition-[width] duration-300 md:top-20 md:block",
          collapsed ? "w-[70px]" : "w-[240px]"
        )}
      >
        <SidebarContent collapsed={collapsed} onToggleCollapse={onToggleCollapse} desktop />
      </aside>

      <div
        className={cn(
          "fixed inset-x-0 bottom-0 top-24 z-40 bg-black/30 transition-opacity md:hidden",
          open ? "opacity-100" : "pointer-events-none opacity-0"
        )}
        onClick={onClose}
      />

      <aside
        className={cn(
          "fixed bottom-0 left-0 top-24 z-50 w-[280px] border-r border-red-100 bg-white shadow-xl transition-transform md:hidden",
          open ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex items-center justify-end px-3 py-3">
          <Button variant="ghost" size="default" onClick={onClose} aria-label="Close sidebar">
            <X size={18} />
          </Button>
        </div>
        <SidebarContent onClose={onClose} />
      </aside>
    </>
  );
}

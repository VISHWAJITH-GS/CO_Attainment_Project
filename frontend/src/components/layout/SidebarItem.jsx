import { NavLink } from "react-router-dom";
import { cn } from "../../lib/utils";

export function SidebarItem({ to, icon: Icon, label, collapsed = false, onNavigate }) {
  return (
    <NavLink
      to={to}
      onClick={onNavigate}
      title={collapsed ? label : undefined}
      className={({ isActive }) =>
        cn(
          "group flex w-full items-center rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
          collapsed ? "justify-center" : "gap-3",
          isActive
            ? "bg-red-100 text-red-900"
            : "text-slate-700 hover:bg-red-50 hover:text-red-900"
        )
      }
    >
      <Icon size={18} className="shrink-0" />
      <span
        className={cn(
          "overflow-hidden whitespace-nowrap transition-all duration-300",
          collapsed ? "max-w-0 opacity-0" : "max-w-[160px] opacity-100"
        )}
      >
        {label}
      </span>
    </NavLink>
  );
}

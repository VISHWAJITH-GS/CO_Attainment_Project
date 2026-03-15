import { User } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from "../ui/dropdown-menu";

export function Navbar({ user, onLogout }) {
  return (
    <header className="sticky top-0 z-30 border-b border-red-100 bg-white">
      <div className="flex h-16 items-center justify-between px-6">

        {/* Branding */}
        <h1 className="text-lg font-semibold text-red-700">
            TCE COAS
        </h1>

        {/* Profile Dropdown */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-slate-800 hover:bg-slate-100">
              <User size={18} />
              {user?.role || "Staff"}
            </button>
          </DropdownMenuTrigger>

          <DropdownMenuContent align="end" className="w-40">

            <DropdownMenuItem>
              Profile
            </DropdownMenuItem>

            <DropdownMenuItem>
              Settings
            </DropdownMenuItem>

            <DropdownMenuItem
              className="text-red-600"
              onClick={onLogout}
            >
              Logout
            </DropdownMenuItem>

          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
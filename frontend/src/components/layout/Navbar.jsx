import { Menu, User } from "lucide-react";
import { Button } from "../ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from "../ui/dropdown-menu";

export function Navbar({ user, onLogout, onMenuClick }) {
  return (
    <header className="fixed inset-x-0 top-0 z-40 border-b border-red-100 bg-white">
      <div className="flex h-24 flex-col justify-center px-4 md:h-20 md:flex-row md:items-center md:justify-between md:px-8">
        <div className="mb-1 flex justify-center md:hidden">
          <img src="/tce-banner.png" alt="TCE Logo" className="h-8 w-auto" />
        </div>

        <div className="flex w-full items-center justify-between md:w-auto md:gap-6">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              className="md:hidden"
              onClick={onMenuClick}
              aria-label="Open sidebar"
            >
              <Menu size={18} />
            </Button>

            <img
              src="/tce-banner.png"
              alt="TCE Logo"
              className="hidden h-12 w-auto md:block"
            />

            <h1 className="text-base font-semibold text-red-700 md:text-xl">
              TCE COAS
            </h1>
          </div>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-slate-800 hover:bg-slate-100 md:py-2.5 md:text-base">
                <User size={18} />
                {user?.role || "Staff"}
              </button>
            </DropdownMenuTrigger>

            <DropdownMenuContent align="end" className="w-40">
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Settings</DropdownMenuItem>
              <DropdownMenuItem
                className="text-red-600"
                onClick={onLogout}
              >
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
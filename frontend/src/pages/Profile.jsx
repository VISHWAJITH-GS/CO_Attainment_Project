import { Building2, IdCard, Mail, ShieldCheck, UserRound } from "lucide-react";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { getProfile } from "../lib/api";

export default function Profile({ user }) {
  const [facultyProfile, setFacultyProfile] = useState({
    name: "Staff User",
    email: user?.email || "",
    department: "Computer Science and Engineering",
    role: user?.role || "Staff",
    employeeId: "TCE-FAC-0000",
  });

  useEffect(() => {
    async function loadProfile() {
      if (!user?.email) {
        return;
      }

      try {
        const data = await getProfile(user.email);
        setFacultyProfile(data);
      } catch {
        setFacultyProfile((prev) => ({
          ...prev,
          email: user.email,
        }));
      }
    }

    loadProfile();
  }, [user?.email]);

  return (
    <div className="space-y-6 p-4 md:p-6">
      <Card className="border-red-100/80 shadow-[0_18px_45px_-35px_rgba(127,29,29,0.45)]">
        <CardHeader className="pb-4">
          <CardTitle className="text-2xl text-red-950">Profile</CardTitle>
          <p className="mt-2 max-w-2xl text-sm text-slate-600">
            View your faculty account details used across the CO Attainment Automation System.
          </p>
        </CardHeader>
      </Card>

      <Card className="mx-auto w-full max-w-4xl border-red-100/80 shadow-[0_18px_35px_-30px_rgba(30,41,59,0.35)]">
        <CardHeader className="pb-5">
          <CardTitle className="flex items-center gap-2 text-xl text-red-950">
            <UserRound size={20} className="text-red-900" />
            Faculty Information
          </CardTitle>
        </CardHeader>

        <CardContent>
          <dl className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border border-slate-200 bg-slate-50/70 p-4">
              <dt className="text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">Name</dt>
              <dd className="mt-2 text-sm font-medium text-slate-900">{facultyProfile.name}</dd>
            </div>

            <div className="rounded-lg border border-slate-200 bg-slate-50/70 p-4">
              <dt className="flex items-center gap-1 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">
                <Mail size={14} /> Email
              </dt>
              <dd className="mt-2 text-sm font-medium text-slate-900">{facultyProfile.email}</dd>
            </div>

            <div className="rounded-lg border border-slate-200 bg-slate-50/70 p-4">
              <dt className="flex items-center gap-1 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">
                <Building2 size={14} /> Department
              </dt>
              <dd className="mt-2 text-sm font-medium text-slate-900">{facultyProfile.department}</dd>
            </div>

            <div className="rounded-lg border border-slate-200 bg-slate-50/70 p-4">
              <dt className="flex items-center gap-1 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">
                <ShieldCheck size={14} /> Role
              </dt>
              <dd className="mt-2 text-sm font-medium text-slate-900">{facultyProfile.role}</dd>
            </div>

            <div className="rounded-lg border border-slate-200 bg-slate-50/70 p-4 sm:col-span-2">
              <dt className="flex items-center gap-1 text-xs font-semibold uppercase tracking-[0.15em] text-slate-500">
                <IdCard size={14} /> Employee ID
              </dt>
              <dd className="mt-2 text-sm font-medium text-slate-900">{facultyProfile.employeeId}</dd>
            </div>
          </dl>
        </CardContent>
      </Card>
    </div>
  );
}
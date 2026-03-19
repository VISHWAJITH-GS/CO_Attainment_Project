import { useState } from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Building2,
  LockKeyhole,
  LogOut,
  Mail,
  ShieldCheck,
  UserRound,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { getProfile, updatePassword } from "../lib/api";

export default function Settings({ user }) {
  const navigate = useNavigate();
  const [facultyProfile, setFacultyProfile] = useState({
    name: "Staff User",
    email: user?.email || "",
    department: "Computer Science and Engineering",
    role: user?.role || "Staff",
  });
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordMessage, setPasswordMessage] = useState("");
  const [messageType, setMessageType] = useState("idle");

  useEffect(() => {
    async function loadProfile() {
      if (!user?.email) {
        return;
      }

      try {
        const profile = await getProfile(user.email);
        setFacultyProfile({
          name: profile.name,
          email: profile.email,
          department: profile.department,
          role: profile.role,
        });
      } catch {
        setFacultyProfile((prev) => ({
          ...prev,
          email: user.email,
        }));
      }
    }

    loadProfile();
  }, [user?.email]);

  const handlePasswordUpdate = (event) => {
    event.preventDefault();

    if (!currentPassword || !newPassword || !confirmPassword) {
      setMessageType("error");
      setPasswordMessage("Please fill all password fields.");
      return;
    }

    if (newPassword.length < 8) {
      setMessageType("error");
      setPasswordMessage("New password must be at least 8 characters.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setMessageType("error");
      setPasswordMessage("New password and confirm password do not match.");
      return;
    }

    updatePassword({
      email: facultyProfile.email,
      currentPassword,
      newPassword,
    })
      .then((data) => {
        setMessageType("success");
        setPasswordMessage(data.message || "Password updated successfully.");
        setCurrentPassword("");
        setNewPassword("");
        setConfirmPassword("");
      })
      .catch((error) => {
        setMessageType("error");
        setPasswordMessage(error.message || "Password update failed.");
      });
  };

  return (
    <div className="space-y-6 p-4 md:p-6">
      <Card className="border-red-100/80 shadow-[0_18px_45px_-35px_rgba(127,29,29,0.45)]">
        <CardHeader className="pb-4">
          <CardTitle className="text-2xl text-red-950">Settings</CardTitle>
          <p className="mt-2 max-w-2xl text-sm text-slate-600">
            Manage your profile details, account security, and session actions within the CO Attainment dashboard.
          </p>
        </CardHeader>
      </Card>

      <div className="mx-auto w-full max-w-4xl space-y-5">
        <Card className="border-red-100/80 shadow-[0_18px_35px_-30px_rgba(30,41,59,0.35)]">
          <CardHeader className="pb-5">
            <CardTitle className="flex items-center gap-2 text-xl text-red-950">
              <UserRound size={20} className="text-red-900" />
              Profile Information
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
            </dl>
          </CardContent>
        </Card>

        <Card className="border-red-100/80 shadow-[0_18px_35px_-30px_rgba(30,41,59,0.35)]">
          <CardHeader className="pb-5">
            <CardTitle className="flex items-center gap-2 text-xl text-red-950">
              <LockKeyhole size={20} className="text-red-900" />
              Change Password
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={handlePasswordUpdate}>
              <div className="space-y-2">
                <Label htmlFor="currentPassword">Current Password</Label>
                <Input
                  id="currentPassword"
                  type="password"
                  value={currentPassword}
                  onChange={(event) => setCurrentPassword(event.target.value)}
                  placeholder="Enter current password"
                />
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="newPassword">New Password</Label>
                  <Input
                    id="newPassword"
                    type="password"
                    value={newPassword}
                    onChange={(event) => setNewPassword(event.target.value)}
                    placeholder="Enter new password"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm New Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(event) => setConfirmPassword(event.target.value)}
                    placeholder="Re-enter new password"
                  />
                </div>
              </div>

              {passwordMessage ? (
                <p
                  className={`text-sm ${
                    messageType === "success" ? "text-emerald-700" : "text-red-700"
                  }`}
                >
                  {passwordMessage}
                </p>
              ) : null}

              <Button type="submit" className="min-w-[170px]">
                Update Password
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card className="border-red-100/80 shadow-[0_18px_35px_-30px_rgba(30,41,59,0.35)]">
          <CardHeader className="pb-5">
            <CardTitle className="flex items-center gap-2 text-xl text-red-950">
              <LogOut size={20} className="text-red-900" />
              Account Actions
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-slate-600">
              End your current session and return to the login page.
            </p>
            <Button
              variant="ghost"
              className="border border-red-200 hover:bg-red-50"
              onClick={() => navigate("/login")}
            >
              Logout
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card className="mx-auto w-full max-w-4xl border-red-100/80 bg-red-50/50">
        <CardContent className="pt-6">
          <p className="text-xs font-medium text-slate-600">
            Tip: Use a strong password containing uppercase letters, lowercase letters, numbers, and special characters.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

export default function Settings() {
  return (
    <div className="space-y-6 p-4 md:p-6">
      <Card className="border-red-100/80">
        <CardHeader>
          <CardTitle className="text-red-950">Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-600">Manage profile preferences and system options.</p>
        </CardContent>
      </Card>
    </div>
  );
}

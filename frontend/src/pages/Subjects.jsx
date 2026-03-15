import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

export default function Subjects() {
  return (
    <div className="space-y-6 p-4 md:p-6">
      <Card className="border-red-100/80">
        <CardHeader>
          <CardTitle className="text-red-950">My Subjects</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-600">Select a subject to upload files and continue CO report generation.</p>
        </CardContent>
      </Card>
    </div>
  );
}

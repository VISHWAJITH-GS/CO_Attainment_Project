import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

export default function Reports() {
  return (
    <div className="space-y-6 p-4 md:p-6">
      <Card className="border-red-100/80">
        <CardHeader>
          <CardTitle className="text-red-950">Reports</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-600">Generate and download CO attainment reports from this section.</p>
        </CardContent>
      </Card>
    </div>
  );
}

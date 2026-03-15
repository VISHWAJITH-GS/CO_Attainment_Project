import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

export default function Dashboard() {
  return (
    <div className="space-y-6 p-4 md:p-6">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          { label: "Courses", value: "42" },
          { label: "Faculty", value: "28" },
          { label: "Assessments", value: "136" },
          { label: "Avg Attainment", value: "78%" },
        ].map((stat) => (
          <Card key={stat.label} className="border-red-100/80">
            <CardContent className="p-5">
              <p className="text-xs uppercase tracking-wide text-slate-500">{stat.label}</p>
              <p className="mt-1 text-3xl font-semibold text-slate-900">{stat.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="border-red-100/80">
        <CardHeader>
          <CardTitle className="text-red-950">Department Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-600">
            This dashboard shell is ready. Next, we can connect real CO attainment data and add page-level routes.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

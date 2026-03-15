import { BookOpen, GraduationCap } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

const assignedSubjects = [
  { code: "CS301", name: "Database Management Systems", semester: "Semester V" },
  { code: "CS302", name: "Design and Analysis of Algorithms", semester: "Semester V" },
  { code: "CS401", name: "Machine Learning", semester: "Semester VII" },
  { code: "CS403", name: "Compiler Design", semester: "Semester VII" },
  { code: "IT305", name: "Software Engineering", semester: "Semester V" },
  { code: "IT407", name: "Cloud Computing", semester: "Semester VII" },
];

export default function Dashboard() {
  return (
    <div className="space-y-6 p-4 md:p-6">
      <Card className="border-red-100/80 shadow-[0_18px_45px_-35px_rgba(127,29,29,0.45)]">
        <CardHeader className="pb-4">
          <div className="flex items-start gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-red-100 text-red-900">
              <GraduationCap size={20} />
            </div>
            <div className="min-w-[220px] flex-1">
              <CardTitle className="text-2xl text-red-950">Staff Dashboard</CardTitle>
              <p className="mt-2 max-w-2xl text-sm text-slate-600">
                Manage your assigned subjects, open each workspace, upload assessment files, configure CO parameters,
                and generate attainment reports.
              </p>
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {assignedSubjects.map((subject) => (
          <Card
            key={subject.code}
            className="border-red-100/80 shadow-[0_18px_35px_-30px_rgba(30,41,59,0.35)] transition hover:-translate-y-0.5 hover:shadow-[0_22px_40px_-30px_rgba(127,29,29,0.5)]"
          >
            <CardHeader className="space-y-3 pb-4">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-red-700">{subject.code}</p>
              <CardTitle className="text-lg leading-6 text-slate-900">{subject.name}</CardTitle>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <BookOpen size={16} className="text-slate-500" />
                <span>{subject.semester}</span>
              </div>

              <Button asChild className="w-full">
                <Link to={`/subjects/${subject.code}/workspace`}>Open Workspace</Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

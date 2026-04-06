import { BookOpen, GraduationCap, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
<<<<<<< HEAD
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import {
  pageVariants,
  containerVariants,
  cardVariants,
  sectionVariants,
} from "../lib/animations";

const assignedSubjects = [
  { code: "CS301", name: "Database Management Systems", semester: "Semester V" },
  { code: "CS302", name: "Design and Analysis of Algorithms", semester: "Semester V" },
  { code: "CS401", name: "Machine Learning", semester: "Semester VII" },
  { code: "CS403", name: "Compiler Design", semester: "Semester VII" },
  { code: "IT305", name: "Software Engineering", semester: "Semester V" },
  { code: "IT407", name: "Cloud Computing", semester: "Semester VII" },
];
=======
import { useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { getSubjects } from "../lib/api";
>>>>>>> bba6283fd97fa492d7caf0417155ff43572a8dcb

export default function Dashboard() {
  const [subjects, setSubjects] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadSubjects() {
      try {
        const data = await getSubjects();
        setSubjects(data || []);
      } catch (loadError) {
        setError(loadError.message || "Failed to load subjects.");
      }
    }

    loadSubjects();
  }, []);

  return (
<<<<<<< HEAD
    <motion.div
      className="space-y-6 p-4 md:p-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
    >
      {/* Header card */}
      <motion.div variants={sectionVariants}>
        <Card className="border-red-100/80 shadow-[0_18px_45px_-35px_rgba(127,29,29,0.45)]">
          <CardHeader className="pb-4">
            <div className="flex items-start gap-3">
              <motion.div
                className="grid h-10 w-10 place-items-center rounded-xl bg-red-100 text-red-900"
                whileHover={{ scale: 1.08, rotate: 4 }}
                transition={{ type: "spring", stiffness: 300, damping: 18 }}
              >
                <GraduationCap size={20} />
              </motion.div>
              <div className="min-w-[220px] flex-1">
                <CardTitle className="text-2xl text-red-950">Staff Dashboard</CardTitle>
                <p className="mt-2 max-w-2xl text-sm text-slate-600">
                  Manage your assigned subjects, open each workspace, upload assessment files, configure CO parameters,
                  and generate attainment reports.
                </p>
=======
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

      {error ? <p className="text-sm text-red-700">{error}</p> : null}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {subjects.map((subject) => (
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
>>>>>>> bba6283fd97fa492d7caf0417155ff43572a8dcb
              </div>
            </div>
          </CardHeader>
        </Card>
      </motion.div>

      {/* Subject grid */}
      <motion.div
        className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {assignedSubjects.map((subject) => (
          <motion.div
            key={subject.code}
            variants={cardVariants}
            whileHover={{ y: -4, transition: { duration: 0.22, ease: "easeOut" } }}
          >
            <Card className="card-hover h-full border-red-100/80 shadow-[0_18px_35px_-30px_rgba(30,41,59,0.35)]">
              <CardHeader className="space-y-3 pb-4">
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-red-700">
                  {subject.code}
                </p>
                <CardTitle className="text-lg leading-6 text-slate-900">{subject.name}</CardTitle>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <BookOpen size={16} className="text-slate-500" />
                  <span>{subject.semester}</span>
                </div>

                <Button asChild className="btn-press w-full group">
                  <Link to={`/subjects/${subject.code}/workspace`}>
                    Open Workspace
                    <ArrowRight
                      size={15}
                      className="ml-1.5 opacity-70 transition-transform duration-200 group-hover:translate-x-1"
                    />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  );
}

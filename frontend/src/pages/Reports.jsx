import { CalendarDays, CircleCheck, Clock3, Download, FileSpreadsheet, Loader2 } from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import {
  pageVariants,
  containerVariants,
  cardVariants,
  sectionVariants,
} from "../lib/animations";

const reports = [
  {
    id: "CS301",
    subjectCode: "CS301",
    subjectName: "Database Management Systems",
    semester: "Semester V",
    generatedOn: "12 Feb 2026",
    status: "Generated",
  },
  {
    id: "CS302",
    subjectCode: "CS302",
    subjectName: "Design and Analysis of Algorithms",
    semester: "Semester V",
    generatedOn: "10 Feb 2026",
    status: "Generated",
  },
  {
    id: "CS401",
    subjectCode: "CS401",
    subjectName: "Machine Learning",
    semester: "Semester VII",
    generatedOn: null,
    status: "Processing",
  },
  {
    id: "CS403",
    subjectCode: "CS403",
    subjectName: "Compiler Design",
    semester: "Semester VII",
    generatedOn: null,
    status: "Pending",
  },
  {
    id: "IT305",
    subjectCode: "IT305",
    subjectName: "Software Engineering",
    semester: "Semester V",
    generatedOn: "08 Feb 2026",
    status: "Generated",
  },
  {
    id: "IT407",
    subjectCode: "IT407",
    subjectName: "Cloud Computing",
    semester: "Semester VII",
    generatedOn: "11 Feb 2026",
    status: "Generated",
  },
];

const statusStyles = {
  Generated: "border-emerald-200 bg-emerald-50 text-emerald-700",
  Pending: "border-amber-200 bg-amber-50 text-amber-700",
  Processing: "border-sky-200 bg-sky-50 text-sky-700",
};

function handleDownloadReport(report) {
  const content = [
    "CO Attainment Report",
    `Subject Code: ${report.subjectCode}`,
    `Subject Name: ${report.subjectName}`,
    `Semester: ${report.semester}`,
    `Status: ${report.status}`,
    `Generated On: ${report.generatedOn || "Not yet generated"}`,
  ].join("\n");

  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${report.subjectCode}_CO_Attainment_Report.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function DownloadButton({ report }) {
  const [loading, setLoading] = useState(false);
  const canDownload = report.status === "Generated";

  const handleClick = () => {
    if (!canDownload) return;
    setLoading(true);
    setTimeout(() => {
      handleDownloadReport(report);
      setLoading(false);
    }, 700);
  };

  return (
    <Button
      className="btn-press w-full"
      disabled={!canDownload || loading}
      onClick={handleClick}
    >
      <AnimatePresence mode="wait" initial={false}>
        {loading ? (
          <motion.span
            key="loading"
            className="flex items-center gap-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <Loader2 size={14} className="spinner" />
            Downloading…
          </motion.span>
        ) : (
          <motion.span
            key="idle"
            className="flex items-center gap-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <Download size={16} />
            Download Report
          </motion.span>
        )}
      </AnimatePresence>
    </Button>
  );
}

export default function Reports() {
  return (
    <motion.div
      className="space-y-6 p-4 md:p-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
    >
      {/* Header */}
      <motion.div variants={sectionVariants}>
        <Card className="border-red-100/80 shadow-[0_18px_45px_-35px_rgba(127,29,29,0.45)]">
          <CardHeader className="pb-4">
            <CardTitle className="text-2xl text-red-950">Reports</CardTitle>
            <p className="mt-2 max-w-2xl text-sm text-slate-600">
              View and download generated CO attainment reports for your assigned subjects.
            </p>
          </CardHeader>
        </Card>
      </motion.div>

      {/* Report cards */}
      <motion.div
        className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {reports.map((report) => (
          <motion.div
            key={report.id}
            variants={cardVariants}
            whileHover={{ y: -4, transition: { duration: 0.22, ease: "easeOut" } }}
          >
            <Card className="card-hover h-full border-red-100/80 shadow-[0_18px_35px_-30px_rgba(30,41,59,0.35)]">
              <CardHeader className="space-y-3 pb-4">
                <div className="flex items-start justify-between gap-3">
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-red-700">
                    {report.subjectCode}
                  </p>

                  <motion.span
                    className={`status-badge inline-flex items-center gap-1 rounded-full border px-2 py-1 text-[11px] font-semibold ${statusStyles[report.status]}`}
                    layout
                  >
                    {report.status === "Generated" ? (
                      <CircleCheck size={12} />
                    ) : report.status === "Processing" ? (
                      <Loader2 size={12} className="spinner" />
                    ) : (
                      <Clock3 size={12} />
                    )}
                    {report.status}
                  </motion.span>
                </div>

                <CardTitle className="text-lg leading-6 text-slate-900">
                  {report.subjectName}
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="space-y-2 text-sm text-slate-600">
                  <p className="font-medium text-slate-700">{report.semester}</p>
                  <p className="flex items-center gap-2">
                    <CalendarDays size={14} className="text-slate-500" />
                    {report.generatedOn
                      ? `Generated: ${report.generatedOn}`
                      : "Generated: Not available yet"}
                  </p>
                </div>

                <DownloadButton report={report} />

                {report.status !== "Generated" && (
                  <p className="text-xs text-slate-500">
                    Report download is enabled once processing is completed.
                  </p>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {/* Footer note */}
      <motion.div variants={sectionVariants}>
        <Card className="border-red-100/80 bg-red-50/50">
          <CardContent>
            <p className="flex items-center gap-2 text-sm text-slate-600">
              <FileSpreadsheet size={16} className="text-red-700" />
              Reports are organized by subject and reflect the latest generated attainment status.
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  );
}

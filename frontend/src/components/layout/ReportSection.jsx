import { FileSpreadsheet, Loader2, CheckCircle2, Download } from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
<<<<<<< HEAD
import { cardVariants } from "../../lib/animations";
=======
import { useState } from "react";
import { downloadReportFile, generateReport } from "../../lib/api";
>>>>>>> bba6283fd97fa492d7caf0417155ff43572a8dcb

export default function ReportSection({
  completed,
  uploadedFiles,
  parametersCompleted,
  onGenerated,
  user,
  subjectCode,
  subjectName,
  semester,
}) {
  const requiredFiles = 7;
<<<<<<< HEAD
  const [generating, setGenerating] = useState(false);
  const [generated, setGenerated] = useState(false);
=======
  const [isGenerating, setIsGenerating] = useState(false);
  const [message, setMessage] = useState("");
>>>>>>> bba6283fd97fa492d7caf0417155ff43572a8dcb

  const uploadedCount = Object.keys(uploadedFiles || {}).length;
  const allUploaded = uploadedCount === requiredFiles;
  const canGenerate = allUploaded && parametersCompleted && !generated;

  const statusMessage = generated
    ? "Report generated successfully! You can now download the output."
    : canGenerate
    ? "Upload and parameter steps are complete. You can generate the report."
    : !allUploaded
    ? `Upload all files to enable report generation (${uploadedCount}/7 uploaded)`
    : "Complete the parameter section to enable report generation.";

<<<<<<< HEAD
  const handleGenerate = () => {
    if (!canGenerate) return;
    setGenerating(true);

    setTimeout(() => {
      setGenerating(false);
      setGenerated(true);
      onGenerated?.();
    }, 1800);
  };
=======
  async function handleGenerate() {
    if (!user?.email || !subjectCode) {
      setMessage("Please log in again.");
      return;
    }

    setIsGenerating(true);
    setMessage("");

    try {
      await generateReport(subjectCode, {
        email: user.email,
        subjectName,
        semester,
      });

      const blob = await downloadReportFile(subjectCode, user.email);
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${subjectCode}_OFFICIAL_REPORT.xlsx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      setMessage("Report generated and downloaded.");
      onGenerated?.();
    } catch (error) {
      setMessage(error.message || "Failed to generate report.");
    } finally {
      setIsGenerating(false);
    }
  }
>>>>>>> bba6283fd97fa492d7caf0417155ff43572a8dcb

  return (
    <motion.div variants={cardVariants}>
      <Card className="border-red-100/80 shadow-[0_16px_35px_-32px_rgba(15,23,42,0.65)]">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-950">
            <FileSpreadsheet size={18} />
            Report Generation Section
            <AnimatePresence>
              {(completed || generated) && (
                <motion.span
                  className="ml-2 flex items-center gap-1 text-xs text-emerald-700"
                  initial={{ opacity: 0, scale: 0.7 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.7 }}
                  transition={{ type: "spring", stiffness: 280, damping: 20 }}
                >
                  <CheckCircle2 size={13} className="text-emerald-600" />
                  Completed
                </motion.span>
              )}
            </AnimatePresence>
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-5">
          {/* Status message */}
          <AnimatePresence mode="wait">
            <motion.p
              key={statusMessage}
              className={`text-sm ${
                generated ? "text-emerald-700 font-medium" : "text-slate-500"
              }`}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.25 }}
            >
              {statusMessage}
            </motion.p>
          </AnimatePresence>

          {/* Generating progress */}
          <AnimatePresence>
            {generating && (
              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
              >
                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <Loader2 size={14} className="spinner text-red-700" />
                  Processing files and computing CO attainment…
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
                  <motion.div
                    className="h-full rounded-full bg-gradient-to-r from-red-700 to-red-400"
                    initial={{ width: "0%" }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 1.6, ease: "easeInOut" }}
                  />
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Action area */}
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm font-medium text-slate-700">
                Generate CO Attainment Report
              </p>
              <p className="text-xs text-slate-500">
                This will process uploaded files and compute final CO attainment.
              </p>
            </div>

            <div className="flex gap-3">
              <motion.div whileTap={canGenerate && !generating ? { scale: 0.97 } : {}}>
                <Button
                  className="btn-press min-w-[200px]"
                  onClick={handleGenerate}
                  disabled={!canGenerate || generating}
                >
                  {generating ? (
                    <span className="flex items-center gap-2">
                      <Loader2 size={14} className="spinner" />
                      Generating…
                    </span>
                  ) : generated ? (
                    <span className="flex items-center gap-2">
                      <CheckCircle2 size={14} />
                      Report Generated
                    </span>
                  ) : (
                    "Generate Report"
                  )}
                </Button>
              </motion.div>

<<<<<<< HEAD
              <AnimatePresence>
                {generated && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.85 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.85 }}
                    transition={{ type: "spring", stiffness: 280, damping: 20 }}
                  >
                    <Button variant="ghost" className="btn-press border border-red-200 hover:bg-red-50">
                      <Download size={15} className="mr-1.5" />
                      Download
                    </Button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
=======
          <Button
            className="min-w-[200px]"
            onClick={handleGenerate}
            disabled={!canGenerate || isGenerating}
          >
            {isGenerating ? "Generating..." : "Generate Report"}
          </Button>

        </div>
        {message ? <p className="w-full text-xs text-slate-600">{message}</p> : null}
      </CardContent>
    </Card>
>>>>>>> bba6283fd97fa492d7caf0417155ff43572a8dcb
  );
}
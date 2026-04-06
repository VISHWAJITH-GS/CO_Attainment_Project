import { useParams } from "react-router-dom";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import FileUploadSection from "../components/layout/FileUploadSection";
import ParameterSection from "../components/layout/ParameterSection";
import ReportSection from "../components/layout/ReportSection";
import { pageVariants, containerVariants, sectionVariants } from "../lib/animations";

const subjectCatalog = {
  CS301: { name: "Database Management Systems", semester: "Semester V" },
  CS302: { name: "Design and Analysis of Algorithms", semester: "Semester V" },
  CS401: { name: "Machine Learning", semester: "Semester VII" },
  CS403: { name: "Compiler Design", semester: "Semester VII" },
  IT305: { name: "Software Engineering", semester: "Semester V" },
  IT407: { name: "Cloud Computing", semester: "Semester VII" },
};

const workflowSteps = [
  { id: 1, label: "Upload Files" },
  { id: 2, label: "Set Parameters" },
  { id: 3, label: "Generate Report" },
  { id: 4, label: "Download" },
];

export default function SubjectWorkspace() {
  const [uploadedFiles, setUploadedFiles] = useState({});
  const [step, setStep] = useState(1);
  const [openSections, setOpenSections] = useState({
    upload: true,
    parameter: false,
  });
  const { subjectCode } = useParams();
  const resolvedSubjectCode = subjectCode || "SUBJECT";
  const details = subjectCatalog[subjectCode] || {
    name: "Subject Name",
    semester: "Semester",
  };

  return (
    <motion.div
      className="space-y-6 p-4 md:p-6"
      variants={pageVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
    >
      {/* Page header */}
      <motion.div
        className="flex flex-wrap items-center justify-between gap-3"
        variants={sectionVariants}
      >
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Subject Workspace
          </p>
          <h1 className="mt-1 text-2xl font-semibold text-red-950">
            {resolvedSubjectCode} — {details.name}
          </h1>
          <p className="mt-1 text-sm font-medium text-slate-600">{details.semester}</p>
          <p className="mt-2 text-sm text-slate-600">
            Upload assessment files, configure CO parameters, generate attainment reports, and download outputs.
          </p>
        </div>
      </motion.div>

      {/* Workflow stepper */}
      <motion.div
        className="rounded-xl border border-red-100 bg-white p-3 shadow-[0_8px_20px_-20px_rgba(127,29,29,0.65)]"
        variants={sectionVariants}
      >
        <ol className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-4">
          {workflowSteps.map((item) => {
            const isActive = step === item.id;
            const isCompleted = step > item.id;

            return (
              <motion.li
                key={item.id}
                className={`flex items-center gap-2 rounded-lg border px-2.5 py-2 text-xs transition-colors duration-300 ${
                  isCompleted
                    ? "border-red-200 bg-red-100/70 text-red-900"
                    : isActive
                    ? "border-red-300 bg-white text-red-800 shadow-sm"
                    : "border-slate-200 bg-white/70 text-slate-500"
                }`}
                layout
                transition={{ duration: 0.25 }}
              >
                <motion.span
                  className={`step-badge grid h-6 w-6 shrink-0 place-items-center rounded-full text-[11px] font-semibold ${
                    isCompleted || isActive
                      ? "bg-red-700 text-white active"
                      : "bg-slate-200 text-slate-600"
                  }`}
                  animate={{
                    scale: isActive ? 1.1 : 1,
                    backgroundColor: isCompleted || isActive ? "#b91c1c" : "#e2e8f0",
                  }}
                  transition={{ duration: 0.3 }}
                >
                  {isCompleted ? "✓" : item.id}
                </motion.span>
                <span className="font-medium leading-tight">{item.label}</span>

                {isActive && (
                  <motion.span
                    className="ml-auto h-1.5 w-1.5 rounded-full bg-red-500"
                    animate={{ opacity: [1, 0.3, 1] }}
                    transition={{ duration: 1.2, repeat: Infinity }}
                  />
                )}
              </motion.li>
            );
          })}
        </ol>
      </motion.div>

      {/* Sections */}
      <motion.div
        className="space-y-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <FileUploadSection
          isOpen={openSections.upload}
          completed={step > 1}
          onToggle={() =>
            setOpenSections((prev) => ({
              ...prev,
              upload: !prev.upload,
            }))
          }
          onUploadChange={(files) => {
            setUploadedFiles(files);

            if (Object.keys(files).length === 7) {
              setStep(2);
              setOpenSections((prev) => ({
                ...prev,
                upload: false,
                parameter: true,
              }));
            }
          }}
        />

        <ParameterSection
          isOpen={openSections.parameter}
          completed={step > 2}
          onToggle={() =>
            setOpenSections((prev) => ({
              ...prev,
              parameter: !prev.parameter,
            }))
          }
          onComplete={() => {
            setStep(3);
            setOpenSections((prev) => ({
              ...prev,
              parameter: false,
            }));
          }}
        />

        <ReportSection
          completed={step > 3}
          uploadedFiles={uploadedFiles}
          parametersCompleted={step >= 3}
          onGenerated={() => setStep(4)}
        />
      </motion.div>
    </motion.div>
  );
}

import { FileSpreadsheet } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export default function ReportSection({ completed, uploadedFiles, parametersCompleted, onGenerated }) {
  const requiredFiles = 7;

  const uploadedCount = Object.keys(uploadedFiles || {}).length;
  const allUploaded = uploadedCount === requiredFiles;
  const canGenerate = allUploaded && parametersCompleted;

  const statusMessage = canGenerate
    ? "Upload and parameter steps are complete. You can generate the report."
    : !allUploaded
    ? `Upload all files to enable report generation (${uploadedCount}/7 uploaded)`
    : "Complete the parameter section to enable report generation.";

  return (
    <Card className="border-red-100/80 shadow-[0_16px_35px_-32px_rgba(15,23,42,0.65)]">

      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-red-950">
          <FileSpreadsheet size={18} />
          Report Generation Section
          {completed && (
            <span className="ml-2 text-xs text-red-900">✔ Completed</span>
          )}
        </CardTitle>
      </CardHeader>

      <CardContent className="flex flex-wrap items-center justify-between gap-4">
        <p className="text-xs text-slate-500">
          {statusMessage}
        </p>
        <div>
          <p className="text-sm font-medium text-slate-700">
            Generate CO Attainment Report
          </p>

          <p className="text-xs text-slate-500">
            This will process uploaded files and compute final CO attainment.
          </p>
        </div>

        <div className="flex gap-3">

          <Button
            className="min-w-[200px]"
            onClick={onGenerated}
            disabled={!canGenerate}
          >
            Generate Report
          </Button>

        </div>
      </CardContent>
    </Card>
  );
}
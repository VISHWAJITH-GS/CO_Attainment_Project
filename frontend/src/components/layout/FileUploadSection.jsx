import { ChevronDown, Upload } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Input } from "../ui/input";
import { useState } from "react";

const uploadFields = [
  { key: "qp", label: "Upload Question Paper" },
  { key: "marks", label: "Upload Student Marks" },
  { key: "cat1", label: "Upload CAT1" },
  { key: "cat2", label: "Upload CAT2" },
  { key: "assignment1", label: "Upload Assignment1" },
  { key: "assignment2", label: "Upload Assignment2" },
  { key: "terminal", label: "Upload Terminal Marks" },
];

export default function FileUploadSection({ isOpen, completed, onUploadChange, onToggle }) {
  const [uploadedFiles, setUploadedFiles] = useState({});
  
  const handleUpload = (key) => {
  const updated = {
    ...uploadedFiles,
    [key]: true,
  };

  setUploadedFiles(updated);

  if (onUploadChange) {
    onUploadChange(updated);
  }
};

  return (
    <Card className="border-red-100/80 shadow-[0_16px_35px_-32px_rgba(15,23,42,0.65)]">
      <CardHeader>
        <div className="flex items-center justify-between gap-3">
          <CardTitle className="flex items-center gap-2 text-red-950">
            <Upload size={18} />
            File Upload Section
            {completed && (
              <span className="ml-2 text-xs text-red-900">✔ Completed</span>
            )}
          </CardTitle>
          <Button variant="ghost" size="default" className="h-8 w-8 p-0" onClick={onToggle} aria-label="Toggle upload section">
            <ChevronDown size={16} className={`transition-transform ${isOpen ? "rotate-180" : "rotate-0"}`} />
          </Button>
        </div>
      </CardHeader>

      {isOpen && (<CardContent className="space-y-4">
        <div className="space-y-2">
  <p className="text-sm font-medium text-slate-700">
    Upload Progress
  </p>

  <div className="w-full h-2 bg-slate-200 rounded-full">
    <div
      className="h-2 bg-red-600 rounded-full"
      style={{
        width: `${
          (Object.keys(uploadedFiles).length / uploadFields.length) * 100
        }%`,
      }}
    ></div>
  </div>

  <p className="text-xs text-slate-500">
    {Object.keys(uploadedFiles).length} / {uploadFields.length} files uploaded
  </p>
</div>
        {uploadFields.map((item) => (
          <div
            key={item.key}
            className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-[1.4fr_2fr_auto_auto] md:items-center"
          >
            <p className="text-sm font-medium text-slate-700">
              {item.label}
            </p>

            <Input type="file" className="bg-slate-50 text-sm" />

            <Button className="w-full md:w-auto" onClick={() => handleUpload(item.key)}>
              Upload
            </Button>

            <span
            className={`text-xs font-medium ${
                uploadedFiles[item.key]
                ? "text-green-600"
                : "text-slate-400"
            }`}
            >
            {uploadedFiles[item.key] ? "Uploaded" : "Not Uploaded"}
            </span>
          </div>
        ))}
      </CardContent>)}
    </Card>
  );
}
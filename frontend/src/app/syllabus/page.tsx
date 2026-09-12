export default function SyllabusPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Syllabus Processing</h1>
        <p className="text-muted-foreground">Upload syllabus documents (PDFs) to extract academic topics and schedules.</p>
      </div>
      <div className="p-12 border border-dashed rounded-xl bg-card text-center flex flex-col items-center justify-center gap-3">
        <p className="font-semibold text-lg">Syllabus Document Upload</p>
        <p className="text-sm text-muted-foreground max-w-sm">
          PDF extraction and processing functionality will connect to the FastAPI backend service.
        </p>
      </div>
    </div>
  );
}


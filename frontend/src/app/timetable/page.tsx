export default function TimetablePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Timetable</h1>
        <p className="text-muted-foreground">View and adjust your personalized study timetable.</p>
      </div>
      <div className="p-12 border rounded-xl bg-card text-center text-muted-foreground">
        No timetable generated yet. Upload a syllabus to auto-generate your study schedule.
      </div>
    </div>
  );
}


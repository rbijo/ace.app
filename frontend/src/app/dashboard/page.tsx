export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Student Dashboard</h1>
        <p className="text-muted-foreground">Overview of academic workload, upcoming study sessions, and progress.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <p className="text-sm font-medium text-muted-foreground">Active Subjects</p>
          <h2 className="text-3xl font-extrabold mt-2">0</h2>
        </div>
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <p className="text-sm font-medium text-muted-foreground">Pending Tasks</p>
          <h2 className="text-3xl font-extrabold mt-2">0</h2>
        </div>
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <p className="text-sm font-medium text-muted-foreground">Study Hours Completed</p>
          <h2 className="text-3xl font-extrabold mt-2">0h</h2>
        </div>
      </div>
    </div>
  );
}


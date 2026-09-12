export default function TasksPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Study Tasks</h1>
        <p className="text-muted-foreground">Manage and track your generated academic study tasks.</p>
      </div>
      <div className="p-12 border rounded-xl bg-card text-center text-muted-foreground">
        No active study tasks.
      </div>
    </div>
  );
}


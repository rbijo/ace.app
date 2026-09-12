import Link from "next/link";
import { GraduationCap, ArrowRight, Calendar, FileText, CheckSquare } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-xs font-semibold text-primary mb-6">
        <GraduationCap className="h-4 w-4" />
        AI Companion for Education
      </div>

      <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight max-w-3xl mb-4">
        Master Your Academic Journey with <span className="text-primary">ACE</span>
      </h1>

      <p className="text-lg text-muted-foreground max-w-2xl mb-8">
        Process syllabus documents, generate adaptive study timetables, manage tasks automatically, and reach your full potential.
      </p>

      <div className="flex flex-wrap gap-4 justify-center mb-16">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 rounded-lg bg-primary px-6 py-3 font-semibold text-primary-foreground hover:bg-primary/90 transition-colors shadow-md"
        >
          Go to Dashboard
          <ArrowRight className="h-4 w-4" />
        </Link>
        <Link
          href="/syllabus"
          className="inline-flex items-center gap-2 rounded-lg border border-input bg-background px-6 py-3 font-semibold hover:bg-accent hover:text-accent-foreground transition-colors"
        >
          Upload Syllabus
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full text-left">
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <FileText className="h-8 w-8 text-primary mb-3" />
          <h3 className="font-bold text-lg mb-2">Syllabus Processing</h3>
          <p className="text-sm text-muted-foreground">
            Extract academic topics, course outlines, and deadlines directly from syllabus PDF uploads.
          </p>
        </div>
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <Calendar className="h-8 w-8 text-primary mb-3" />
          <h3 className="font-bold text-lg mb-2">Adaptive Timetables</h3>
          <p className="text-sm text-muted-foreground">
            Generate conflict-free study timetables tailored to your schedule and progress.
          </p>
        </div>
        <div className="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
          <CheckSquare className="h-8 w-8 text-primary mb-3" />
          <h3 className="font-bold text-lg mb-2">Smart Task Management</h3>
          <p className="text-sm text-muted-foreground">
            Break complex course requirements into manageable daily study tasks and review sessions.
          </p>
        </div>
      </div>
    </div>
  );
}


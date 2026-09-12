import Link from "next/link";
import { GraduationCap, LayoutDashboard, Calendar, FileText, CheckSquare, LogIn } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
      <div className="container max-w-7xl mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 font-bold text-xl text-primary">
          <GraduationCap className="h-7 w-7 text-primary" />
          <span>ACE</span>
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          <Link href="/dashboard" className="flex items-center gap-1.5 hover:text-primary transition-colors">
            <LayoutDashboard className="h-4 w-4" />
            Dashboard
          </Link>
          <Link href="/timetable" className="flex items-center gap-1.5 hover:text-primary transition-colors">
            <Calendar className="h-4 w-4" />
            Timetable
          </Link>
          <Link href="/syllabus" className="flex items-center gap-1.5 hover:text-primary transition-colors">
            <FileText className="h-4 w-4" />
            Syllabus
          </Link>
          <Link href="/tasks" className="flex items-center gap-1.5 hover:text-primary transition-colors">
            <CheckSquare className="h-4 w-4" />
            Tasks
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          <Link
            href="/login"
            className="inline-flex items-center gap-1.5 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors shadow-sm"
          >
            <LogIn className="h-4 w-4" />
            Sign In
          </Link>
        </div>
      </div>
    </header>
  );
}


export function Footer() {
  return (
    <footer className="w-full border-t bg-card py-6 mt-auto">
      <div className="container max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 px-4 text-xs text-muted-foreground">
        <p>&copy; {new Date().getFullYear()} ACE — AI Companion for Education. All rights reserved.</p>
        <p className="flex items-center gap-4">
          <span>Planning & Foundation Phase</span>
        </p>
      </div>
    </footer>
  );
}


"use client";

export default function LoginPage() {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="w-full max-w-md p-8 space-y-6 border rounded-xl bg-card shadow-sm">
        <div className="space-y-2 text-center">
          <h1 className="text-2xl font-bold">Sign In to ACE</h1>
          <p className="text-sm text-muted-foreground">Supabase Authentication Integration</p>
        </div>
        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
          <div className="space-y-2">
            <label className="text-sm font-medium">Email</label>
            <input
              type="email"
              placeholder="student@example.com"
              className="w-full px-3 py-2 border rounded-md bg-background"
              disabled
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full px-3 py-2 border rounded-md bg-background"
              disabled
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 bg-primary text-primary-foreground font-semibold rounded-md opacity-75 cursor-not-allowed"
            disabled
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}


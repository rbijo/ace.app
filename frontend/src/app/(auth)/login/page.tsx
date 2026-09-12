"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { env } from "@/lib/env";
import { LogIn, UserPlus, AlertCircle, CheckCircle2, ShieldCheck } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);

    try {
      if (isSignUp) {
        // Live Supabase Signup Request
        const supabaseRes = await fetch(`${env.supabaseUrl}/auth/v1/signup`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "apikey": env.supabaseAnonKey,
          },
          body: JSON.stringify({
            email,
            password,
            data: { full_name: fullName },
          }),
        });

        if (!supabaseRes.ok) {
          const data = await supabaseRes.json().catch(() => ({}));
          throw new Error(data.msg || data.message || data.error_description || "Supabase registration failed");
        }

        const supabaseData = await supabaseRes.json();
        if (supabaseData.access_token) {
          localStorage.setItem("ace_token", supabaseData.access_token);
        }
        localStorage.setItem("ace_user_email", email);
        setSuccess("Connected to Live Supabase! Account created successfully. Redirecting...");
      } else {
        // Live Supabase Login Request
        const loginRes = await fetch(`${env.supabaseUrl}/auth/v1/token?grant_type=password`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "apikey": env.supabaseAnonKey,
          },
          body: JSON.stringify({ email, password }),
        });

        if (!loginRes.ok) {
          const data = await loginRes.json().catch(() => ({}));
          throw new Error(data.error_description || data.msg || data.message || "Invalid email or password");
        }

        const tokenData = await loginRes.json();
        localStorage.setItem("ace_token", tokenData.access_token);
        localStorage.setItem("ace_user_email", email);
        setSuccess("Signed in to Live Supabase! Redirecting to Dashboard...");
      }

      setTimeout(() => {
        router.push("/dashboard");
      }, 1000);
    } catch (err: any) {
      setError(err.message || "An unexpected authentication error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center py-12">
      <div className="w-full max-w-md p-8 space-y-6 border rounded-xl bg-card shadow-md">
        <div className="space-y-2 text-center">
          <div className="inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary mb-2">
            <ShieldCheck className="h-3.5 w-3.5" />
            Supabase Live Database Connected
          </div>
          <h1 className="text-2xl font-bold">{isSignUp ? "Create an ACE Account" : "Sign In to ACE"}</h1>
          <p className="text-sm text-muted-foreground">
            {isSignUp ? "Register with Supabase Auth" : "Access your study timetables and progress"}
          </p>
        </div>

        {error && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-destructive/15 text-destructive text-sm font-medium">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-green-500/15 text-green-600 dark:text-green-400 text-sm font-medium">
            <CheckCircle2 className="h-4 w-4 shrink-0" />
            <span>{success}</span>
          </div>
        )}

        <form className="space-y-4" onSubmit={handleSubmit}>
          {isSignUp && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Full Name</label>
              <input
                type="text"
                placeholder="Alex Student"
                className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
            </div>
          )}

          <div className="space-y-2">
            <label className="text-sm font-medium">Email Address</label>
            <input
              type="email"
              placeholder="student@example.com"
              className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 py-2.5 bg-primary text-primary-foreground font-semibold rounded-md hover:bg-primary/90 transition-colors shadow-sm disabled:opacity-50"
          >
            {loading ? (
              <span>Processing...</span>
            ) : isSignUp ? (
              <>
                <UserPlus className="h-4 w-4" />
                <span>Sign Up with Supabase</span>
              </>
            ) : (
              <>
                <LogIn className="h-4 w-4" />
                <span>Sign In with Supabase</span>
              </>
            )}
          </button>
        </form>

        <div className="text-center pt-2 border-t">
          <button
            type="button"
            className="text-sm text-primary hover:underline font-medium"
            onClick={() => {
              setIsSignUp(!isSignUp);
              setError(null);
              setSuccess(null);
            }}
          >
            {isSignUp ? "Already have an account? Sign In" : "Don't have an account? Sign Up"}
          </button>
        </div>
      </div>
    </div>
  );
}

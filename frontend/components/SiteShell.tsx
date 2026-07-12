'use client';

import Link from 'next/link';

export function SiteShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <Link href="/" className="text-xl font-semibold text-slate-900">
            AI Job Hunter
          </Link>
          <nav className="flex flex-wrap items-center gap-3 text-sm font-medium text-slate-700">
            <Link href="/dashboard" className="rounded-full px-4 py-2 transition hover:bg-slate-100">
              Dashboard
            </Link>
            <Link href="/jobs" className="rounded-full px-4 py-2 transition hover:bg-slate-100">
              Jobs
            </Link>
            <Link href="/resume-upload" className="rounded-full px-4 py-2 transition hover:bg-slate-100">
              Resume Upload
            </Link>
            <Link href="/resume-match-results" className="rounded-full px-4 py-2 transition hover:bg-slate-100">
              Match Results
            </Link>
            <Link href="/bookmarks" className="rounded-full px-4 py-2 transition hover:bg-slate-100">
              Bookmarks
            </Link>
            <Link href="/settings" className="rounded-full px-4 py-2 transition hover:bg-slate-100">
              Settings
            </Link>
          </nav>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}

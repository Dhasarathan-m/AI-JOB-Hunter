export default function DashboardPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-3xl font-semibold text-slate-900">Dashboard</h1>
            <p className="mt-2 text-slate-600">Track your job search and resume matching progress in one place.</p>
          </div>
        </div>

        <div className="mt-8 grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Job Listings</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Live</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Resume Uploads</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Ready</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Saved Jobs</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Flexible</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Resume Matches</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Insights</p>
          </div>
        </div>
      </div>
    </main>
  );
}

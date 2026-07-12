import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
        <div className="sm:flex sm:items-center sm:justify-between">
          <div>
            <h1 className="text-4xl font-semibold text-slate-900">AI Job Hunter</h1>
            <p className="mt-3 max-w-2xl text-lg text-slate-600">
              Discover jobs, upload your resume, and match against the best listings.
            </p>
          </div>
          <div className="mt-6 flex gap-3 sm:mt-0">
            <Link href="/jobs" className="rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-700">
              Browse Jobs
            </Link>
            <Link href="/resume-upload" className="rounded-full border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-50">
              Upload Resume
            </Link>
          </div>
        </div>

        <div className="mt-10 grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Jobs available</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Live feed</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Resume uploads</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Fast and simple</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Match results</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Actionable insights</p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-medium text-slate-500">Saved jobs</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">Bookmark favorites</p>
          </div>
        </div>

        <div className="mt-10 grid gap-6 xl:grid-cols-2">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Live Job Listings</h2>
            <p className="mt-2 text-slate-600">
              Connect directly to the AI Job Hunter backend and browse current job opportunities.
            </p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Resume Matching</h2>
            <p className="mt-2 text-slate-600">
              Upload your resume and get matching scores, recommendations, and gaps from the backend.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}

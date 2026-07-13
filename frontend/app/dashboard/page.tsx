'use client';

import { useMemo } from 'react';
import { JobCard } from '../../components/JobCard';
import { ErrorBanner } from '../../components/ErrorBanner';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { useJobs } from '../../hooks/useJobs';

export default function DashboardPage() {
  const { jobs, isLoading, error } = useJobs();
  const featuredJobs = useMemo(() => jobs.slice(0, 3), [jobs]);

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
            <p className="text-sm font-medium text-slate-500">Jobs available</p>
            <p className="mt-4 text-3xl font-semibold text-slate-900">{isLoading ? '...' : jobs.length}</p>
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

        <div className="mt-8 rounded-3xl border border-slate-200 bg-slate-50 p-8">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-slate-900">Live job listings</h2>
              <p className="mt-2 text-slate-600">Fresh opportunities pulled from the backend API.</p>
            </div>
          </div>

          {isLoading ? (
            <div className="mt-6 flex justify-center py-8">
              <LoadingSpinner />
            </div>
          ) : error ? (
            <div className="mt-6">
              <ErrorBanner message={error} />
            </div>
          ) : jobs.length === 0 ? (
            <div className="mt-6 rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center text-slate-600">
              No jobs are currently available from the backend.
            </div>
          ) : (
            <div className="mt-6 grid gap-4">
              {featuredJobs.map((job, index) => (
                <JobCard key={`${job.apply_link}-${index}`} job={job} />
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { JobCard } from '../../components/JobCard';
import { useLocalStorage } from '../../hooks/useLocalStorage';
import { useJobs } from '../../hooks/useJobs';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export default function BookmarksPage() {
  const { jobs, isLoading } = useJobs();
  const [bookmarked, setBookmarked] = useLocalStorage<string[]>('bookmarkedJobs', []);
  const [bookmarkedJobs, setBookmarkedJobs] = useState<typeof jobs>([]);

  useEffect(() => {
    setBookmarkedJobs(jobs.filter((job) => bookmarked.includes(job.apply_link)));
  }, [jobs, bookmarked]);

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-semibold text-slate-900">Bookmarked Jobs</h1>
        <p className="mt-2 text-slate-600">Your saved opportunities are stored in the browser for quick access.</p>

        {isLoading ? (
          <div className="mt-8 flex justify-center py-20">
            <LoadingSpinner />
          </div>
        ) : bookmarkedJobs.length === 0 ? (
          <div className="mt-8 rounded-3xl border border-dashed border-slate-300 bg-slate-50 p-10 text-center text-slate-600">
            No bookmarked jobs yet. Browse the job listings to save your favorites.
          </div>
        ) : (
          <div className="mt-8 grid gap-4">
            {bookmarkedJobs.map((job, index) => (
              <JobCard key={`${job.apply_link}-${index}`} job={job} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

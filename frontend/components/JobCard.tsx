'use client';

import Link from 'next/link';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { Job } from '../types';

export function JobCard({ job }: { job: Job }) {
  const [bookmarked, setBookmarked] = useLocalStorage<string[]>('bookmarkedJobs', []);
  const isBookmarked = bookmarked.includes(job.apply_link);

  const toggleBookmark = () => {
    const updated = isBookmarked ? bookmarked.filter((link) => link !== job.apply_link) : [...bookmarked, job.apply_link];
    setBookmarked(updated);
  };

  return (
    <article className="rounded-3xl border border-slate-200 bg-slate-50 p-6 transition hover:shadow-lg">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">{job.title}</h2>
          <p className="mt-2 text-slate-600">{job.company} • {job.location}</p>
        </div>
        <button onClick={toggleBookmark} className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:border-slate-400">
          {isBookmarked ? 'Bookmarked' : 'Bookmark'}
        </button>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <span className="rounded-2xl bg-white px-4 py-2 text-sm font-medium text-slate-700">{job.experience || 'Experience N/A'}</span>
        <span className="rounded-2xl bg-white px-4 py-2 text-sm font-medium text-slate-700">{job.salary || 'Salary N/A'}</span>
        <span className="rounded-2xl bg-white px-4 py-2 text-sm font-medium text-slate-700">Source: {job.source}</span>
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <Link href={`/jobs/${encodeURIComponent(job.apply_link)}`} className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-700">
          View details
        </Link>
        <a href={job.apply_link} target="_blank" rel="noreferrer" className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:border-slate-400">
          Apply externally
        </a>
      </div>
    </article>
  );
}

'use client';

import { useState } from 'react';
import { ErrorBanner } from '../../components/ErrorBanner';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { matchResume, getMatches } from '../../lib/api';

export default function ResumeMatchResultsPage() {
  const [resumeId, setResumeId] = useState('');
  const [matches, setMatches] = useState<any[]>([]);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleMatch = async () => {
    setError(null);
    setResult(null);
    setMatches([]);
    setIsLoading(true);

    try {
      const id = Number(resumeId);
      const data = await matchResume(id);
      setMatches(data.matches);
      setResult(`Matched resume ${data.resume_id}`);
    } catch (err) {
      setError((err as Error).message || 'Resume matching failed.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFetch = async () => {
    setError(null);
    setResult(null);
    setMatches([]);
    setIsLoading(true);

    try {
      const id = Number(resumeId);
      const data = await getMatches(id);
      setMatches(data.matches);
      setResult(`Found ${data.matches.length} stored matches for resume ${data.resume_id}.`);
    } catch (err) {
      setError((err as Error).message || 'Fetching matches failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
        <h1 className="text-3xl font-semibold text-slate-900">Resume Match Results</h1>
        <p className="mt-2 text-slate-600">Enter a resume ID to view the latest match results or fetch stored matches.</p>

        <div className="mt-8 grid gap-4 sm:grid-cols-[1fr_auto]">
          <input
            value={resumeId}
            onChange={(event) => setResumeId(event.target.value)}
            type="number"
            placeholder="Resume ID"
            className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
          />
          <div className="flex gap-3">
            <button onClick={handleMatch} disabled={isLoading} className="rounded-full bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60">
              Match Resume
            </button>
            <button onClick={handleFetch} disabled={isLoading} className="rounded-full border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60">
              Load Stored Matches
            </button>
          </div>
        </div>

        {error && <div className="mt-6"><ErrorBanner message={error} /></div>}
        {result && <div className="mt-6 rounded-3xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-900">{result}</div>}
        {isLoading && <div className="mt-6"><LoadingSpinner /></div>}

        {matches.length > 0 && (
          <div className="mt-8 grid gap-4">
            {matches.map((match, index) => (
              <div key={index} className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
                <p className="text-sm font-medium text-slate-500">Job ID {match.job_id}</p>
                <p className="mt-2 text-2xl font-semibold text-slate-900">Score {match.match_score}</p>
                <p className="mt-2 text-slate-600">{match.recommendation}</p>
                <div className="mt-4 grid gap-2 sm:grid-cols-2">
                  <p className="rounded-2xl bg-white p-3 text-sm font-medium text-slate-700">Matched skills: {match.matched_skills.join(', ') || 'None'}</p>
                  <p className="rounded-2xl bg-white p-3 text-sm font-medium text-slate-700">Missing skills: {match.missing_skills.join(', ') || 'None'}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

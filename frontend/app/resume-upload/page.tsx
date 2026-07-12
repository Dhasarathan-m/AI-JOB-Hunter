'use client';

import { useState } from 'react';
import { ErrorBanner } from '../../components/ErrorBanner';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { uploadResume } from '../../lib/api';

export default function ResumeUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!file) {
      setError('Please choose a resume file.');
      return;
    }

    setError(null);
    setResult(null);
    setIsLoading(true);

    try {
      const data = await uploadResume(file);
      setResult(`Uploaded ${data.filename}. Resume ID: ${data.resume_id}`);
    } catch (err) {
      setError((err as Error).message || 'Resume upload failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
        <h1 className="text-3xl font-semibold text-slate-900">Resume Upload</h1>
        <p className="mt-2 text-slate-600">Upload your PDF or DOCX resume to get matched against available jobs.</p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {error && <ErrorBanner message={error} />}
          {result && <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-900">{result}</div>}

          <label className="block rounded-3xl border border-slate-200 bg-slate-50 p-5">
            <span className="text-sm font-medium text-slate-700">Select resume</span>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              className="mt-4 w-full text-slate-900"
            />
          </label>

          <button
            type="submit"
            disabled={isLoading}
            className="inline-flex items-center justify-center rounded-full bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? <LoadingSpinner /> : 'Upload Resume'}
          </button>
        </form>
      </div>
    </main>
  );
}

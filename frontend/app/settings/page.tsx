'use client';

import { useState } from 'react';

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState('http://127.0.0.1:8000');

  return (
    <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
        <h1 className="text-3xl font-semibold text-slate-900">Settings</h1>
        <p className="mt-2 text-slate-600">Configure frontend behavior and backend API settings.</p>

        <div className="mt-8 grid gap-4">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
            <label className="text-sm font-medium text-slate-700">API Base URL</label>
            <input
              value={apiUrl}
              onChange={(event) => setApiUrl(event.target.value)}
              className="mt-3 w-full rounded-3xl border border-slate-200 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
            />
            <p className="mt-3 text-sm text-slate-500">By default the app uses the local FastAPI backend.</p>
          </div>
        </div>
      </div>
    </main>
  );
}

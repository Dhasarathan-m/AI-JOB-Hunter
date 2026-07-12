'use client';

export function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="rounded-3xl border border-rose-200 bg-rose-50 p-4 text-rose-900">
      <p className="text-sm font-medium">Error</p>
      <p className="mt-1 text-sm">{message}</p>
    </div>
  );
}

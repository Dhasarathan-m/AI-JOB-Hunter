'use client';

export function LoadingSpinner() {
  return (
    <div className="inline-flex items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-300 border-t-slate-900" />
    </div>
  );
}

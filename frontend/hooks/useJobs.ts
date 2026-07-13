'use client';

import { useEffect, useState } from 'react';
import type { Job } from '../types';
import { fetchJobs } from '../lib/api';

export function useJobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const loadJobs = async () => {
      try {
        const data = await fetchJobs();
        if (isMounted) {
          setJobs(data);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Unable to load jobs.');
          setJobs([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    void loadJobs();

    return () => {
      isMounted = false;
    };
  }, []);

  return { jobs, isLoading, error };
}

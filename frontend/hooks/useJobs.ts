'use client';

import { useEffect, useState } from 'react';
import { Job } from '../types';
import { fetchJobs } from '../lib/api';

export function useJobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    fetchJobs()
      .then((data) => {
        if (isMounted) {
          setJobs(data);
          setError(null);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError((err as Error).message);
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return { jobs, isLoading, error };
}

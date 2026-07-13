'use client';

import type { Job, MatchResponse, ResumeUploadResponse } from '../types';

function getApiBaseUrl(): string {
  const configuredUrl = process.env.NEXT_PUBLIC_API_URL?.trim();
  return configuredUrl ? configuredUrl.replace(/\/$/, '') : 'http://127.0.0.1:8000';
}

export async function fetchJobs(): Promise<Job[]> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/jobs`, {
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to load jobs from the backend.');
  }

  return (await response.json()) as Job[];
}

export async function uploadResume(file: File): Promise<ResumeUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${getApiBaseUrl()}/resume/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorMessage = await response.text();
    throw new Error(`Upload failed: ${errorMessage}`);
  }

  return response.json();
}

export async function matchResume(resumeId: number): Promise<MatchResponse> {
  const response = await fetch(`${getApiBaseUrl()}/resume/match?resume_id=${resumeId}`, {
    method: 'POST',
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Match failed: ${body}`);
  }

  return response.json();
}

export async function getMatches(resumeId: number): Promise<MatchResponse> {
  const response = await fetch(`${getApiBaseUrl()}/resume/matches?resume_id=${resumeId}`);

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Failed to load matches: ${body}`);
  }

  return response.json();
}

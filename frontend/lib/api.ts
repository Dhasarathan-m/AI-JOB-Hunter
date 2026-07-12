'use client';

import { Job, ResumeUploadResponse, MatchResponse } from '../types';

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

export async function fetchJobs(): Promise<Job[]> {
  const response = await fetch(`${BASE_URL}/api/v1/jobs`);
  if (!response.ok) {
    throw new Error('Failed to load jobs.');
  }
  return response.json();
}

export async function uploadResume(file: File): Promise<ResumeUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${BASE_URL}/resume/upload`, {
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
  const response = await fetch(`${BASE_URL}/resume/match?resume_id=${resumeId}`, {
    method: 'POST',
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Match failed: ${body}`);
  }

  return response.json();
}

export async function getMatches(resumeId: number): Promise<MatchResponse> {
  const response = await fetch(`${BASE_URL}/resume/matches?resume_id=${resumeId}`);

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Failed to load matches: ${body}`);
  }

  return response.json();
}

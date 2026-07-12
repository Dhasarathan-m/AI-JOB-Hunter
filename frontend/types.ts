export interface Job {
  title: string;
  company: string;
  location: string;
  experience?: string | null;
  salary?: string | null;
  description?: string | null;
  apply_link: string;
  source: string;
  posted_date?: string | null;
}

export interface ResumeUploadResponse {
  resume_id: number;
  filename: string;
  parsed_data: Record<string, any>;
  created_at: string;
}

export interface MatchRecord {
  job_id: number;
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  experience_match: string;
  education_match: string;
  recommendation: string;
  priority: string;
  explanation: string;
  created_at: string;
}

export interface MatchResponse {
  resume_id: number;
  matches: MatchRecord[];
}

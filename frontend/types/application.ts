export const APPLICATION_STATUSES = [
  "applied",
  "interviewing",
  "offer",
  "rejected",
  "withdrawn",
] as const;

export type ApplicationStatus = (typeof APPLICATION_STATUSES)[number];

export interface JobApplication {
  id: string;
  userId: string;
  company: string;
  role: string;
  status: ApplicationStatus;
  location?: string;
  jobUrl?: string;
  salaryRange?: string;
  notes?: string;
  dateApplied?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateApplicationInput {
  company: string;
  role: string;
  status: ApplicationStatus;
  location?: string;
  jobUrl?: string;
  salaryRange?: string;
  notes?: string;
  dateApplied?: string;
}

export type UpdateApplicationInput = Partial<CreateApplicationInput>;

export const RESUME_STATUSES = [
  "uploaded",
  "parsed",
  "parse_failed",
] as const;

export type ResumeStatus = (typeof RESUME_STATUSES)[number];

export interface ResumeDocument {
  id: string;
  userId: string;
  fileName: string;
  fileUrl: string;
  storagePath: string;
  contentType: string;
  sizeBytes: number;
  status: ResumeStatus;
  parsedText?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateResumeMetadataInput {
  fileName: string;
  fileUrl: string;
  storagePath: string;
  contentType: string;
  sizeBytes: number;
  status: ResumeStatus;
}

export interface UpdateResumeMetadataInput {
  fileName?: string;
  fileUrl?: string;
  storagePath?: string;
  contentType?: string;
  sizeBytes?: number;
  status?: ResumeStatus;
  parsedText?: string;
}

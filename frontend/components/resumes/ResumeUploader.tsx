"use client";

import {
  getDownloadURL,
  ref,
  uploadBytesResumable,
  type UploadTaskSnapshot,
} from "firebase/storage";
import { useRef, useState, type ChangeEvent, type FormEvent } from "react";
import { useAuth } from "@/hooks/useAuth";
import { createResumeMetadata } from "@/services/resume-api";
import { storage } from "@/services/firebase";
import { Button } from "@/components/ui/Button";
import styles from "./ResumeUploader.module.scss";

const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024;

const SUPPORTED_FILE_TYPES = new Set([
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain",
]);

const SUPPORTED_FILE_EXTENSIONS = new Set(["pdf", "docx", "txt"]);

function getFileExtension(fileName: string): string {
  return fileName.split(".").pop()?.toLowerCase() ?? "";
}

function sanitizeFileName(fileName: string): string {
  return fileName
    .trim()
    .replace(/\s+/g, "-")
    .replace(/[^a-zA-Z0-9._-]/g, "")
    .toLowerCase();
}

function isSupportedFile(file: File): boolean {
  return (
    SUPPORTED_FILE_TYPES.has(file.type) ||
    SUPPORTED_FILE_EXTENSIONS.has(getFileExtension(file.name))
  );
}

function validateFile(file: File): string | null {
  if (!isSupportedFile(file)) {
    return "Upload a PDF, DOCX, or TXT resume.";
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    return "Resume files must be 5 MB or smaller.";
  }

  return null;
}

interface ResumeUploaderProps {
  onUploadComplete?: () => void;
}

export function ResumeUploader({ onUploadComplete }: ResumeUploaderProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const { user } = useAuth();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;

    setSuccessMessage(null);
    setError(null);
    setUploadProgress(0);
    setSelectedFile(file);

    if (!file) {
      return;
    }

    const validationError = validateFile(file);

    if (validationError) {
      setError(validationError);
      setSelectedFile(null);
    }
  }

  function handleProgress(snapshot: UploadTaskSnapshot) {
    const progress = Math.round(
      (snapshot.bytesTransferred / snapshot.totalBytes) * 100,
    );
    setUploadProgress(progress);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!user) {
      setError("You must be logged in to upload a resume.");
      return;
    }

    if (!selectedFile) {
      setError("Choose a resume file before uploading.");
      return;
    }

    const validationError = validateFile(selectedFile);

    if (validationError) {
      setError(validationError);
      return;
    }

    const uploadId = crypto.randomUUID();
    const safeFileName = sanitizeFileName(selectedFile.name);
    const storagePath = `users/${user.uid}/resumes/${uploadId}/${safeFileName}`;

    try {
      setIsUploading(true);
      setUploadProgress(0);

      const uploadTask = uploadBytesResumable(
        ref(storage, storagePath),
        selectedFile,
        {
          contentType: selectedFile.type || undefined,
        },
      );

      const fileUrl = await new Promise<string>((resolve, reject) => {
        uploadTask.on(
          "state_changed",
          handleProgress,
          reject,
          async () => {
            const downloadUrl = await getDownloadURL(uploadTask.snapshot.ref);
            resolve(downloadUrl);
          },
        );
      });

      await createResumeMetadata({
        contentType: selectedFile.type || "application/octet-stream",
        fileName: selectedFile.name,
        fileUrl,
        sizeBytes: selectedFile.size,
        status: "uploaded",
        storagePath,
      });

      setSelectedFile(null);
      setUploadProgress(100);
      setSuccessMessage("Resume uploaded and saved.");
      inputRef.current?.form?.reset();
      onUploadComplete?.();
    } catch (uploadError) {
      setError(
        uploadError instanceof Error
          ? uploadError.message
          : "Unable to upload resume. Please try again.",
      );
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <form className={styles.uploader} onSubmit={handleSubmit}>
      <div className={styles.header}>
        <h2>Upload resume</h2>
        <p>Store a PDF, DOCX, or TXT resume for future job matching.</p>
      </div>

      <label className={styles.dropzone} htmlFor="resume-file">
        <span className={styles.dropzoneTitle}>
          {selectedFile ? selectedFile.name : "Choose a resume file"}
        </span>
        <span className={styles.dropzoneMeta}>
          PDF, DOCX, or TXT. Maximum 5 MB.
        </span>
        <input
          accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
          className={styles.fileInput}
          disabled={isUploading}
          id="resume-file"
          onChange={handleFileChange}
          ref={inputRef}
          type="file"
        />
      </label>

      {selectedFile ? (
        <dl className={styles.fileDetails}>
          <div>
            <dt>File type</dt>
            <dd>{selectedFile.type || "Unknown"}</dd>
          </div>
          <div>
            <dt>Size</dt>
            <dd>{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</dd>
          </div>
        </dl>
      ) : null}

      {isUploading ? (
        <div className={styles.progressWrap} aria-live="polite">
          <progress
            className={styles.progress}
            max="100"
            value={uploadProgress}
          />
          <span className={styles.progressText}>{uploadProgress}%</span>
        </div>
      ) : null}

      {error ? (
        <p className={styles.error} role="alert">
          {error}
        </p>
      ) : null}

      {successMessage ? (
        <p className={styles.success} role="status">
          {successMessage}
        </p>
      ) : null}

      <div className={styles.actions}>
        <Button disabled={isUploading || !selectedFile} type="submit">
          {isUploading ? "Uploading..." : "Upload resume"}
        </Button>
      </div>
    </form>
  );
}

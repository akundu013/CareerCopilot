"use client";

import { useRouter } from "next/navigation";
import { useState, type ChangeEvent, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { createApplication } from "@/services/application-api";
import {
  APPLICATION_STATUSES,
  type ApplicationStatus,
  type CreateApplicationInput,
} from "@/types/application";
import styles from "./ApplicationForm.module.scss";

const STATUS_LABELS: Record<ApplicationStatus, string> = {
  applied: "Applied",
  interviewing: "Interviewing",
  offer: "Offer",
  rejected: "Rejected",
  withdrawn: "Withdrawn",
};

interface ApplicationFormState {
  company: string;
  role: string;
  status: ApplicationStatus;
  location: string;
  jobUrl: string;
  salaryRange: string;
  dateApplied: string;
  notes: string;
}

const initialFormState: ApplicationFormState = {
  company: "",
  role: "",
  status: "applied",
  location: "",
  jobUrl: "",
  salaryRange: "",
  dateApplied: "",
  notes: "",
};

function optionalValue(value: string): string | undefined {
  const trimmedValue = value.trim();

  return trimmedValue ? trimmedValue : undefined;
}

export function ApplicationForm() {
  const router = useRouter();
  const [form, setForm] = useState<ApplicationFormState>(initialFormState);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateField(
    field: keyof ApplicationFormState,
    value: ApplicationFormState[keyof ApplicationFormState],
  ) {
    setForm((currentForm) => ({
      ...currentForm,
      [field]: value,
    }));
  }

  function handleTextChange(
    field: keyof Omit<ApplicationFormState, "status">,
  ) {
    return (
      event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    ) => {
      updateField(field, event.target.value);
    };
  }

  function handleStatusChange(event: ChangeEvent<HTMLSelectElement>) {
    updateField("status", event.target.value as ApplicationStatus);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    const company = form.company.trim();
    const role = form.role.trim();

    if (!company || !role) {
      setError("Company and role are required.");
      return;
    }

    const payload: CreateApplicationInput = {
      company,
      role,
      status: form.status,
      location: optionalValue(form.location),
      jobUrl: optionalValue(form.jobUrl),
      salaryRange: optionalValue(form.salaryRange),
      dateApplied: optionalValue(form.dateApplied),
      notes: optionalValue(form.notes),
    };

    try {
      setIsSubmitting(true);
      await createApplication(payload);
      router.push("/dashboard/applications");
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Unable to create application. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.grid}>
        <Input
          id="company"
          label="Company"
          onChange={handleTextChange("company")}
          placeholder="Acme Inc."
          required
          value={form.company}
        />
        <Input
          id="role"
          label="Role"
          onChange={handleTextChange("role")}
          placeholder="Frontend Engineer"
          required
          value={form.role}
        />
        <label className={styles.field} htmlFor="status">
          <span className={styles.label}>Status</span>
          <select
            className={styles.control}
            id="status"
            onChange={handleStatusChange}
            value={form.status}
          >
            {APPLICATION_STATUSES.map((status) => (
              <option key={status} value={status}>
                {STATUS_LABELS[status]}
              </option>
            ))}
          </select>
        </label>
        <Input
          id="location"
          label="Location"
          onChange={handleTextChange("location")}
          placeholder="Remote, Toronto, New York"
          value={form.location}
        />
        <Input
          id="jobUrl"
          label="Job URL"
          onChange={handleTextChange("jobUrl")}
          placeholder="https://company.com/jobs/frontend-engineer"
          type="url"
          value={form.jobUrl}
        />
        <Input
          id="salaryRange"
          label="Salary Range"
          onChange={handleTextChange("salaryRange")}
          placeholder="$90k - $120k"
          value={form.salaryRange}
        />
        <Input
          id="dateApplied"
          label="Date Applied"
          onChange={handleTextChange("dateApplied")}
          type="date"
          value={form.dateApplied}
        />
      </div>

      <label className={styles.field} htmlFor="notes">
        <span className={styles.label}>Notes</span>
        <textarea
          className={`${styles.control} ${styles.textarea}`}
          id="notes"
          onChange={handleTextChange("notes")}
          placeholder="Recruiter name, follow-up plan, interview notes, or anything worth remembering."
          value={form.notes}
        />
      </label>

      {error ? (
        <p className={styles.error} role="alert">
          {error}
        </p>
      ) : null}

      <div className={styles.actions}>
        <Button href="/dashboard" variant="secondary">
          Cancel
        </Button>
        <Button disabled={isSubmitting} type="submit">
          {isSubmitting ? "Saving..." : "Save application"}
        </Button>
      </div>
    </form>
  );
}

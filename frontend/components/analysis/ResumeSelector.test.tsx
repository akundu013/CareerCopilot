import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import type { ResumeDocument } from "@/types/resume";
import { ResumeSelector } from "./ResumeSelector";

const resumes: ResumeDocument[] = [
  {
    id: "resume-1",
    userId: "user-1",
    fileName: "Frontend Resume.pdf",
    fileUrl: "https://example.com/frontend.pdf",
    storagePath: "users/user-1/resumes/frontend.pdf",
    contentType: "application/pdf",
    sizeBytes: 1200,
    status: "parsed",
    createdAt: "2026-05-01T00:00:00Z",
    updatedAt: "2026-05-01T00:00:00Z",
  },
  {
    id: "resume-2",
    userId: "user-1",
    fileName: "Backend Resume.pdf",
    fileUrl: "https://example.com/backend.pdf",
    storagePath: "users/user-1/resumes/backend.pdf",
    contentType: "application/pdf",
    sizeBytes: 1500,
    status: "parsed",
    createdAt: "2026-05-02T00:00:00Z",
    updatedAt: "2026-05-02T00:00:00Z",
  },
];

describe("ResumeSelector", () => {
  it("renders resume options and reports selected resume id", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();

    render(
      <ResumeSelector
        onChange={onChange}
        resumes={resumes}
        value=""
      />,
    );

    await user.selectOptions(screen.getByLabelText("Parsed resume"), "resume-2");

    expect(screen.getByRole("option", { name: "Frontend Resume.pdf" }))
      .toBeInTheDocument();
    expect(onChange).toHaveBeenCalledWith("resume-2");
  });
});

import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { JobDescriptionInput } from "./JobDescriptionInput";

describe("JobDescriptionInput", () => {
  it("renders a required textarea and reports changes", () => {
    const onChange = vi.fn();

    render(
      <JobDescriptionInput
        onChange={onChange}
        value=""
      />,
    );

    const textarea = screen.getByLabelText("Job description");

    expect(textarea).toBeRequired();
    fireEvent.change(textarea, {
      target: { value: "React and TypeScript role" },
    });

    expect(onChange).toHaveBeenLastCalledWith("React and TypeScript role");
  });

  it("supports disabled form state", () => {
    render(
      <JobDescriptionInput
        disabled
        onChange={vi.fn()}
        value="Existing description"
      />,
    );

    expect(screen.getByLabelText("Job description")).toBeDisabled();
  });
});

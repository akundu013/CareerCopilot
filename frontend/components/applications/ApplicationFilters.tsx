import {
  APPLICATION_STATUSES,
  type ApplicationStatus,
} from "@/types/application";
import styles from "./ApplicationTable.module.scss";

export type ApplicationStatusFilter = ApplicationStatus | "all";

const FILTER_LABELS: Record<ApplicationStatusFilter, string> = {
  all: "All",
  applied: "Applied",
  interviewing: "Interviewing",
  offer: "Offer",
  rejected: "Rejected",
  withdrawn: "Withdrawn",
};

interface ApplicationFiltersProps {
  activeFilter: ApplicationStatusFilter;
  onFilterChange: (filter: ApplicationStatusFilter) => void;
}

const filters: ApplicationStatusFilter[] = ["all", ...APPLICATION_STATUSES];

export function ApplicationFilters({
  activeFilter,
  onFilterChange,
}: ApplicationFiltersProps) {
  return (
    <div className={styles.filters} aria-label="Application status filters">
      {filters.map((filter) => (
        <button
          aria-pressed={activeFilter === filter}
          className={
            activeFilter === filter
              ? `${styles.filterButton} ${styles.activeFilter}`
              : styles.filterButton
          }
          key={filter}
          onClick={() => onFilterChange(filter)}
          type="button"
        >
          {FILTER_LABELS[filter]}
        </button>
      ))}
    </div>
  );
}

import type { CSSProperties } from "react";
import type { ApplicationsByStatusItem } from "@/types/analytics";
import styles from "./ApplicationsByStatusChart.module.scss";

interface ApplicationsByStatusChartProps {
  data: ApplicationsByStatusItem[];
}

function formatStatus(status: string): string {
  return status
    .split(/[-_\s]+/)
    .filter(Boolean)
    .map((part) => `${part[0]?.toUpperCase() ?? ""}${part.slice(1)}`)
    .join(" ");
}

function getBarStyle(count: number, maxCount: number): CSSProperties {
  const size = maxCount > 0 ? Math.max((count / maxCount) * 100, 8) : 0;

  return { "--bar-size": `${size}%` } as CSSProperties;
}

export function ApplicationsByStatusChart({
  data,
}: ApplicationsByStatusChartProps) {
  const maxCount = Math.max(...data.map((item) => item.count), 0);

  return (
    <section className={styles.chart} aria-labelledby="status-chart-title">
      <div className={styles.header}>
        <h2 id="status-chart-title">Applications by Status</h2>
        <p>Pipeline distribution across your tracked roles.</p>
      </div>

      {data.length ? (
        <div className={styles.rows}>
          {data.map((item) => (
            <div className={styles.row} key={item.status}>
              <div className={styles.rowHeader}>
                <span>{formatStatus(item.status)}</span>
                <strong>{item.count}</strong>
              </div>
              <span
                aria-hidden="true"
                className={styles.track}
                style={getBarStyle(item.count, maxCount)}
              >
                <span className={styles.bar} />
              </span>
            </div>
          ))}
        </div>
      ) : (
        <p className={styles.empty}>No applications tracked yet.</p>
      )}
    </section>
  );
}

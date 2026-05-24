import type { CSSProperties } from "react";
import type { WeeklyApplicationActivityItem } from "@/types/analytics";
import styles from "./WeeklyActivityChart.module.scss";

interface WeeklyActivityChartProps {
  data: WeeklyApplicationActivityItem[];
}

function formatWeek(value: string): string {
  const date = new Date(`${value}T00:00:00`);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
  });
}

function getColumnStyle(count: number, maxCount: number): CSSProperties {
  const size = maxCount > 0 ? Math.max((count / maxCount) * 100, 12) : 0;

  return { "--column-size": `${size}%` } as CSSProperties;
}

export function WeeklyActivityChart({ data }: WeeklyActivityChartProps) {
  const maxCount = Math.max(...data.map((item) => item.count), 0);

  return (
    <section className={styles.chart} aria-labelledby="weekly-chart-title">
      <div className={styles.header}>
        <h2 id="weekly-chart-title">Weekly Application Activity</h2>
        <p>Applications grouped by the week they were created.</p>
      </div>

      {data.length ? (
        <div className={styles.columns}>
          {data.map((item) => (
            <div className={styles.columnWrap} key={item.week}>
              <div className={styles.columnFrame}>
                <span
                  aria-label={`${item.count} applications in week ${item.week}`}
                  className={styles.column}
                  style={getColumnStyle(item.count, maxCount)}
                />
              </div>
              <strong>{item.count}</strong>
              <span>{formatWeek(item.week)}</span>
            </div>
          ))}
        </div>
      ) : (
        <p className={styles.empty}>No weekly application activity yet.</p>
      )}
    </section>
  );
}

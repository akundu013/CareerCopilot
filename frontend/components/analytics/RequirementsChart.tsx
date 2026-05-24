import type { CSSProperties } from "react";
import type { RequirementFrequencyItem } from "@/types/analytics";
import styles from "./RequirementsChart.module.scss";

interface RequirementsChartProps {
  data: RequirementFrequencyItem[];
  description: string;
  emptyMessage: string;
  title: string;
}

function getBarStyle(count: number, maxCount: number): CSSProperties {
  const size = maxCount > 0 ? Math.max((count / maxCount) * 100, 8) : 0;

  return { "--bar-size": `${size}%` } as CSSProperties;
}

export function RequirementsChart({
  data,
  description,
  emptyMessage,
  title,
}: RequirementsChartProps) {
  const maxCount = Math.max(...data.map((item) => item.count), 0);
  const titleId = `${title.toLowerCase().replaceAll(/\s+/g, "-")}-title`;

  return (
    <section className={styles.chart} aria-labelledby={titleId}>
      <div className={styles.header}>
        <h2 id={titleId}>{title}</h2>
        <p>{description}</p>
      </div>

      {data.length ? (
        <div className={styles.rows}>
          {data.map((item) => (
            <div className={styles.row} key={item.requirement}>
              <div className={styles.rowHeader}>
                <span>{item.requirement}</span>
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
        <p className={styles.empty}>{emptyMessage}</p>
      )}
    </section>
  );
}

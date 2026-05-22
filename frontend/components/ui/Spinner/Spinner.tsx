import styles from "./Spinner.module.scss";

interface SpinnerProps {
  label?: string;
}

export function Spinner({ label = "Loading" }: SpinnerProps) {
  return <span aria-label={label} className={styles.spinner} role="status" />;
}

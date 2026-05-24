from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.demo_reset_service import reset_demo_data


def main() -> None:
    counts = reset_demo_data()

    print("Reset demo data:")
    for label, count in counts.items():
        print(f"- {label}: {count}")


if __name__ == "__main__":
    main()

from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.demo_seed_data import seed_demo_data


def main() -> None:
    counts = seed_demo_data()

    print("Seeded demo data:")
    for collection_name, count in counts.items():
        print(f"- {collection_name}: {count}")


if __name__ == "__main__":
    main()

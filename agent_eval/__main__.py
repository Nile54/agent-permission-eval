import argparse
import json
from pathlib import Path

from .runner import evaluate, markdown_report


def main():
    parser = argparse.ArgumentParser(description="Run the simulated authorization experiment")
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    result = evaluate()
    report = markdown_report(result)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "baseline.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.output / "baseline.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()

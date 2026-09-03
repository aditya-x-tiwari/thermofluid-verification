import argparse
import json
from pathlib import Path

from gemini_analyzer import analyze_pdf
from figure_extractor import render_pages


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pdf",
        required=True
    )

    parser.add_argument(
        "--output",
        default="output"
    )

    args = parser.parse_args()

    pdf = Path(args.pdf)
    output = Path(args.output)

    output.mkdir(parents=True, exist_ok=True)

    print("Analyzing paper with Gemini...")

    spec = analyze_pdf(str(pdf))

    json_path = output / "validation_spec.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            spec.model_dump(),
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved: {json_path}")

    print("Rendering paper pages...")

    figures_dir = output / "paper_pages"

    render_pages(
        str(pdf),
        str(figures_dir)
    )

    print("Analysis complete.")


if __name__ == "__main__":
    main()
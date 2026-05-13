import argparse
import csv
from datetime import datetime
from pathlib import Path


DEFAULT_INPUT = Path("data/sample_trend.csv")
DEFAULT_OUTPUT = Path("output/trend.svg")


def read_trend_csv(csv_path):
    dates = []
    values = []

    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required_columns = {"date", "value"}
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain 'date' and 'value' columns.")

        for row in reader:
            dates.append(datetime.strptime(row["date"], "%Y-%m-%d"))
            values.append(float(row["value"]))

    if not dates:
        raise ValueError("CSV does not contain any data rows.")

    return dates, values


def scale_points(values, width, height, padding):
    min_value = min(values)
    max_value = max(values)
    value_range = max_value - min_value or 1
    x_step = (width - padding * 2) / max(len(values) - 1, 1)

    points = []
    for index, value in enumerate(values):
        x = padding + index * x_step
        y = height - padding - ((value - min_value) / value_range) * (height - padding * 2)
        points.append((x, y))

    return points, min_value, max_value


def build_svg(dates, values):
    width = 720
    height = 420
    padding = 64
    points, min_value, max_value = scale_points(values, width, height, padding)
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    baseline = height - padding

    point_marks = []
    for date, value, (x, y) in zip(dates, values, points):
        point_marks.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#2563eb" />'
        )
        point_marks.append(
            f'<text x="{x:.1f}" y="{y - 12:.1f}" text-anchor="middle" '
            f'font-size="12" fill="#1f2937">{value:g}</text>'
        )
        point_marks.append(
            f'<text x="{x:.1f}" y="{baseline + 28:.1f}" text-anchor="middle" '
            f'font-size="11" fill="#64748b">{date.strftime("%m월")}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff" />
  <text x="{width / 2}" y="34" text-anchor="middle" font-size="22" font-weight="700" fill="#111827">Monthly Value Trend</text>
  <line x1="{padding}" y1="{baseline}" x2="{width - padding}" y2="{baseline}" stroke="#cbd5e1" />
  <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{baseline}" stroke="#cbd5e1" />
  <text x="24" y="{padding + 4}" font-size="12" fill="#64748b">{max_value:g}</text>
  <text x="24" y="{baseline + 4}" font-size="12" fill="#64748b">{min_value:g}</text>
  <polyline points="{polyline}" fill="none" stroke="#2563eb" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
  {"".join(point_marks)}
</svg>
"""


def save_trend_graph(dates, values, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_svg(dates, values), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Read a CSV file with date,value columns and save a trend graph."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="CSV file path")
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT, help="Output SVG file path"
    )
    args = parser.parse_args()

    dates, values = read_trend_csv(args.input)
    save_trend_graph(dates, values, args.output)
    print(f"Saved trend graph to {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate direct three-point ARC commands in the Plant 3D script."""

from pathlib import Path
import sys


EPSILON = 1e-9


def parse_point(token: str) -> tuple[float, float]:
    parts = token.split(",")
    if len(parts) != 2:
        raise ValueError(f"expected x,y point, got {token!r}")
    return float(parts[0]), float(parts[1])


def twice_triangle_area(a, b, c) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def main() -> int:
    default_script = Path(__file__).resolve().parents[1] / "plant3d_pfd_template.scr"
    script_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_script

    errors: list[str] = []
    arc_count = 0

    for line_number, raw_line in enumerate(script_path.read_text(encoding="utf-8").splitlines(), 1):
        code = raw_line.split(";", 1)[0].strip()
        if not code.upper().startswith("_.ARC"):
            continue

        arc_count += 1
        parts = code.split()
        if len(parts) != 4:
            errors.append(
                f"line {line_number}: expected '_.ARC start second end', got {code!r}"
            )
            continue

        try:
            a, b, c = (parse_point(token) for token in parts[1:])
        except ValueError as exc:
            errors.append(f"line {line_number}: {exc}")
            continue

        area2 = twice_triangle_area(a, b, c)
        if abs(area2) <= EPSILON:
            errors.append(
                f"line {line_number}: collinear ARC points: "
                f"{parts[1]} {parts[2]} {parts[3]}"
            )
            continue

        print(
            f"OK line {line_number}: {parts[1]} {parts[2]} {parts[3]} "
            f"(twice-area={abs(area2):g})"
        )

    if arc_count == 0:
        errors.append("no _.ARC commands found")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {arc_count} ARC command(s): no collinear 3-point definitions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

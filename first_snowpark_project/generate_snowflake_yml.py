#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


DEFAULT_RUNTIME = "3.10"
RUNTIME_PATTERN = re.compile(r"^\d+\.\d+$")


def build_config(template_path: Path, runtime: str) -> str:
    if not RUNTIME_PATTERN.match(runtime):
        raise ValueError(
            f"Invalid runtime '{runtime}'. Expected format like '3.10' or '3.11'."
        )

    template = template_path.read_text(encoding="utf-8")
    return template.replace("__PY_RUNTIME__", runtime)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate snowflake.yml from template with a single runtime value."
    )
    parser.add_argument(
        "--runtime",
        default=os.getenv("PY_RUNTIME", DEFAULT_RUNTIME),
        help="Python runtime version (example: 3.10). Defaults to PY_RUNTIME env var or 3.10.",
    )
    parser.add_argument(
        "--template",
        default="snowflake.template.yml",
        help="Template file path.",
    )
    parser.add_argument(
        "--output",
        default="snowflake.yml",
        help="Output file path.",
    )

    args = parser.parse_args()
    template_path = Path(args.template)
    output_path = Path(args.output)

    generated = build_config(template_path=template_path, runtime=args.runtime)
    output_path.write_text(generated, encoding="utf-8")
    print(f"Generated {output_path} with runtime {args.runtime}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

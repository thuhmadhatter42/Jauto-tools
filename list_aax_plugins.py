#!/usr/bin/env python3
"""
List every *.aaxplugin in a chosen folder and export the names to a CSV.
Works on macOS, Windows, and Linux.

Usage:
    python list_aax_plugins.py
"""

import csv
import sys
from pathlib import Path


def prompt_path(prompt_message: str, must_exist: bool = True) -> Path:
    """
    Prompt user for a path and return it as a pathlib.Path object.
    Accepts paths copied from the shell that contain '\ ' escape sequences.
    """
    while True:
        raw = input(prompt_message).strip().strip('"').strip("'")
        raw = raw.replace("\\ ", " ")      # turn "\ " into literal space
        p = Path(raw)

        if must_exist and not p.exists():
            print("Path does not exist. Try again.\n")
            continue
        return p


def main() -> None:
    print("\nAAX Plugin Lister ➜ export names to CSV\n")

    # 1. Where are the plugins?
    plugin_dir = prompt_path("Enter path to your AAX Plug-Ins folder: ")

    # 2. Gather *.aaxplugin items (non-recursive)
    plugins = sorted(
        f.name for f in plugin_dir.iterdir()
        if f.suffix.lower() == ".aaxplugin" and f.is_dir()
    )

    if not plugins:
        print("No .aaxplugin items found in that location.")
        sys.exit(0)

    # 3. Where should the CSV go?
    csv_path = prompt_path(
        "Enter full path (including filename.csv) for export: ", must_exist=False
    )
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # 4. Write CSV
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Plugin Name"])
        writer.writerows([[p] for p in plugins])

    print(f"\n✓ Exported {len(plugins)} plugin names to: {csv_path}")


if __name__ == "__main__":
    main()

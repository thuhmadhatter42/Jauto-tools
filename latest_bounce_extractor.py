#!/usr/bin/env python3
import os
import shutil
import time
from pathlib import Path
from datetime import datetime

DEST_DIR = Path.home() / "Desktop" / "Collected Bounces"
DEST_DIR.mkdir(parents=True, exist_ok=True)

def list_mounted_drives():
    return [f for f in os.listdir("/Volumes") if os.path.isdir(os.path.join("/Volumes", f))]

def find_bounced_dirs(root):
    for dirpath, dirnames, _ in os.walk(root):
        for dirname in dirnames:
            if dirname.lower() == "bounced files":
                yield os.path.join(dirpath, dirname)

def get_files_by_ext(folder, extension):
    return [
        os.path.join(folder, f) for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(extension)
    ]

def copy_files(files, dest_root):
    total = len(files)
    for i, f in enumerate(files, 1):
        dest_file = dest_root / f"{Path(f).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{Path(f).suffix}"
        shutil.copy2(f, dest_file)
        print_progress(i, total)

def print_progress(current, total):
    bar_len = 40
    filled = int(bar_len * current / total)
    bar = "█" * filled + "-" * (bar_len - filled)
    print(f"\r🔄 [{bar}] {current}/{total} files copied", end="", flush=True)
    if current == total:
        print()

def menu_select(prompt, options):
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    while True:
        choice = input("Select an option by number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]

def main():
    input("🚀 Press ENTER to start extracting bounces...")

    # Drive selection
    drives = list_mounted_drives()
    if not drives:
        print("❌ No drives found.")
        return
    drive = menu_select("Select a drive:", drives)
    search_root = f"/Volumes/{drive}"

    # Format selection
    file_type = menu_select("Select bounce file format:", [".wav", ".mp3", ".aif"])

    # Count selection
    while True:
        bounce_input = input("How many recent bounces do you want per session? (e.g. 1, 5, 9999): ").strip()
        if bounce_input.isdigit() and int(bounce_input) > 0:
            bounce_limit = int(bounce_input)
            break

    print(f"\n🔍 Searching for {file_type} bounces in: {search_root}\n")
    all_files_to_copy = []
    total_scanned = 0

    for bounced_dir in find_bounced_dirs(search_root):
        files = get_files_by_ext(bounced_dir, file_type)
        total_scanned += len(files)
        files.sort(key=lambda x: os.path.getctime(x), reverse=True)
        all_files_to_copy.extend(files[:bounce_limit])

    if all_files_to_copy:
        copy_files(all_files_to_copy, DEST_DIR)
        print(f"\n✅ Copied {len(all_files_to_copy)} files to: {DEST_DIR}")
    else:
        print("⚠️ No matching files found.")

    print(f"📊 Total scanned: {total_scanned} {file_type.upper()} files")

if __name__ == "__main__":
    main()

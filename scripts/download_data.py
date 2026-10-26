"""Download and extract the SSA national and state baby-name files.

Usage:
    python scripts/download_data.py            # both files, skip if present
    python scripts/download_data.py --state    # state file only
    python scripts/download_data.py --force    # re-download

If SSA refuses the scripted request (HTTP 403), download the zip in a web
browser, save it under data/raw/ with its original name (names.zip or
namesbystate.zip), and run this script again: it will extract it.
"""

from __future__ import annotations

import argparse
import sys

from names_project.data import NATIONAL_URL, STATE_URL, DownloadError, Paths, download_file, extract_zip


def fetch(url: str, target_dir, force: bool) -> bool:
    paths = Paths()
    archive = paths.raw / url.rsplit("/", 1)[-1]
    if target_dir.exists() and any(target_dir.iterdir()) and not force:
        print(f"[skip] {target_dir} already contains files (use --force to refresh)")
        return True
    try:
        download_file(url, archive, overwrite=force)
    except DownloadError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return False
    files = extract_zip(archive, target_dir)
    print(f"[ok] extracted {len(files)} files from {archive.name} into {target_dir}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--national", action="store_true", help="only the national file")
    parser.add_argument("--state", action="store_true", help="only the state file")
    parser.add_argument("--force", action="store_true", help="re-download even if files exist")
    args = parser.parse_args()
    both = not (args.national or args.state)
    paths = Paths()
    ok = True
    if both or args.national:
        ok &= fetch(NATIONAL_URL, paths.national_raw, args.force)
    if both or args.state:
        ok &= fetch(STATE_URL, paths.state_raw, args.force)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

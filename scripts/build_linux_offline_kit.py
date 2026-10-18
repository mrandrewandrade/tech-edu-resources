from __future__ import annotations

import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "offline-kits" / "linux"
OUTPUT = ROOT / "site" / "assets" / "linux" / "TEJ-Linux-Offline-Kit.zip"
QUICK_START = ROOT / "site" / "assets" / "linux" / "TEJ-Linux-Offline-Kit-Quick-Start.pdf"
MANIFEST = SOURCE / "SHA256SUMS.txt"
FIXED_TIME = (2026, 10, 18, 0, 0, 0)


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCE.rglob("*")
        if path.is_file() and path != MANIFEST
    )


def write_manifest(files: list[Path]) -> None:
    lines = []
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        relative = path.relative_to(SOURCE).as_posix()
        lines.append(f"{digest}  {relative}")
    quick_start_digest = hashlib.sha256(QUICK_START.read_bytes()).hexdigest()
    lines.append(f"{quick_start_digest}  PRINTABLE-QUICK-START.pdf")
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def build_zip() -> None:
    files = source_files()
    write_manifest(files)
    files.append(MANIFEST)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(files):
            relative = Path("TEJ-Linux-Offline-Kit") / path.relative_to(SOURCE)
            info = ZipInfo(relative.as_posix(), date_time=FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o644 & 0xFFFF) << 16
            if path.name.endswith(".sh"):
                info.external_attr = (0o755 & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())

        quick_start_info = ZipInfo(
            "TEJ-Linux-Offline-Kit/PRINTABLE-QUICK-START.pdf",
            date_time=FIXED_TIME,
        )
        quick_start_info.compress_type = ZIP_DEFLATED
        quick_start_info.external_attr = (0o644 & 0xFFFF) << 16
        archive.writestr(quick_start_info, QUICK_START.read_bytes())


if __name__ == "__main__":
    build_zip()
    print(f"Built {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")

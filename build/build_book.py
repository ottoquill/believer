#!/usr/bin/env python3
"""Assemble BELIEVER into a single manuscript and build EPUB + DOCX via pandoc.

Order: pandoc auto title page (from metadata.yaml) -> front matter -> parts/chapters
-> back matter. Parts are H1 dividers; chapters/interludes are H2 (own EPUB files).
"""
import os
import re
import subprocess
import sys

ROOT = "/home/paul/git/ottoquill/believer"
CH = f"{ROOT}/manuscript/chapters"
MATTER = f"{ROOT}/manuscript/matter"
BUILD = f"{ROOT}/build"

FRONT = [
    f"{MATTER}/00-copyright.md",
    f"{MATTER}/01-dedication.md",
    f"{MATTER}/02-epigraph.md",
]
BACK = [
    f"{MATTER}/90-about-author.md",
    f"{MATTER}/91-acknowledgments.md",
    f"{MATTER}/92-discussion-questions.md",
]

# Parts -> ordered unit ids
PARTS = [
    ("Part One — The Wince",        ["ch01", "ch02", "intA", "ch03", "ch04", "ch05", "intB"]),
    ("Part Two — Proximity",        ["ch06", "ch07", "ch08", "intC", "ch09"]),
    ("Part Three — The Public Square", ["ch10", "ch11", "intD", "ch12", "ch13", "ch14", "intE", "ch15"]),
    ("Part Four — The Creed",       ["ch16", "ch17", "intF", "ch18", "intG", "ch19", "intH", "ch20"]),
    ("Part Five — Reckoning",       ["ch21", "ch22", "intI", "ch23", "ch24", "ch25"]),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def normalize_chapter(text):
    """Ensure the unit begins with an H2 and no stray top-level headings."""
    lines = text.splitlines()
    # demote any accidental single-# heading at the very top to ##
    if lines and re.match(r"^#\s+", lines[0]):
        lines[0] = "#" + lines[0]  # # -> ##
    return "\n".join(lines).strip()


def wordcount(text):
    # strip headings/markdown punctuation roughly
    t = re.sub(r"[#*_>`]", " ", text)
    return len(t.split())


def main():
    missing = []
    all_ids = [u for _, ids in PARTS for u in ids]
    for uid in all_ids:
        if not os.path.exists(f"{CH}/{uid}.md"):
            missing.append(uid)
    if missing:
        print("MISSING chapter files:", ", ".join(missing), file=sys.stderr)
        sys.exit(2)

    pieces = []
    total_words = 0

    for path in FRONT:
        pieces.append(read(path))

    for part_title, ids in PARTS:
        pieces.append(f"# {part_title}")
        for uid in ids:
            body = normalize_chapter(read(f"{CH}/{uid}.md"))
            total_words += wordcount(body)
            pieces.append(body)

    for path in BACK:
        pieces.append(read(path))

    master = "\n\n\n".join(pieces) + "\n"
    master_path = f"{BUILD}/Believer.md"
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master)

    print(f"Assembled {master_path}")
    print(f"Manuscript body word count (chapters only): ~{total_words:,}")

    common = [
        "pandoc",
        f"{BUILD}/metadata.yaml",
        master_path,
        "--from", "markdown+smart",
        "--toc", "--toc-depth=2",
        "--top-level-division=part",
    ]

    # EPUB
    epub_cmd = common + [
        "--epub-chapter-level=2",
        "--css", f"{BUILD}/epub.css",
        "-o", f"{BUILD}/Believer.epub",
    ]
    subprocess.run(epub_cmd, check=True, cwd=BUILD)
    print("Built Believer.epub")

    # DOCX
    docx_cmd = common + ["-o", f"{BUILD}/Believer.docx"]
    subprocess.run(docx_cmd, check=True, cwd=BUILD)
    print("Built Believer.docx")


if __name__ == "__main__":
    main()

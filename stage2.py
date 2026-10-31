import time

INPUT_TXT = "stage1.txt"
CLEAN_TXT = "stage2.txt"

# Distinct line prefixes that belong to the CET Cell header block
HEADER_PREFIXES = (
    "State Common Entrance Test Cell",
    "First Year Under Graduate Technical Courses",
    "Admissions A.Y.",
    "Final Merit List Maharashtra State Candidates",
    "Note : $ - Indicates that Candidate",
    "# - Indicates that Candidate",
    "Note :- For PWD Candidates",
)


def clean_headers(input_file: str, output_file: str):
    start = time.time()
    print(f"[*] Reading and cleaning '{input_file}'...")

    kept_lines = []
    removed_count = 0

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Check if this line starts with any known header sentence
            if any(stripped.startswith(prefix) for prefix in HEADER_PREFIXES):
                removed_count += 1
                continue

            # Skip standalone footnote / receipt symbol remnants
            if stripped in ("$", "@", "#", "$#", "@#"):
                removed_count += 1
                continue

            kept_lines.append(line)

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(kept_lines)

    elapsed = time.time() - start
    print(f"[✓] Done in {elapsed:.2f}s!")
    print(f"[✓] Removed {removed_count:,} header/note lines.")
    print(f"[✓] Cleaned file saved to: '{output_file}'")


if __name__ == "__main__":
    clean_headers(INPUT_TXT, CLEAN_TXT)

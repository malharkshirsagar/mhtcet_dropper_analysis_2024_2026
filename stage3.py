import re
import time

INPUT_TXT = "stage2.txt"  # Output from Stage 2
OUTPUT_TXT = "stage3.txt"

# Matches patterns like 'Page 1 of 4958' or 'Page 105 of 4958'
PAGE_NUM_PATTERN = re.compile(r"Page\s+\d+\s+of\s+\d+", re.IGNORECASE)


def remove_footers(input_path: str, output_path: str):
    start = time.time()
    print(f"[*] Removing footers and page delimiters from '{input_path}'...")

    kept_lines = []
    removed_count = 0

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Skip empty blank lines between pages
            if not stripped:
                continue

            # 1. Matches "Published on DD/MM/YYYY..." lines
            if stripped.startswith("Published on"):
                removed_count += 1
                continue

            # 2. Matches the page delimiter banner from Stage 1
            if stripped.startswith("--- PAGE") and stripped.endswith("END ---"):
                removed_count += 1
                continue

            # 3. Matches standalone "Page X of Y" lines if line wrapped
            if PAGE_NUM_PATTERN.search(stripped):
                removed_count += 1
                continue

            kept_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as out:
        out.writelines(kept_lines)

    elapsed = time.time() - start
    print(f"[✓] Completed in {elapsed:.2f} seconds!")
    print(f"[✓] Removed {removed_count:,} footer/delimiter lines.")
    print(f"[✓] Saved cleaned data to: '{output_path}'")


if __name__ == "__main__":
    remove_footers(INPUT_TXT, OUTPUT_TXT)

import re
import time

INPUT_FILE = "stage4.txt"  # Your current cleaned file
OUTPUT_FILE = "stage5.txt"  # Output with zero empty gaps


def compress_to_continuous(input_path: str, output_path: str):
    start = time.time()
    print(f"[*] Compressing lines and removing blank gaps from '{input_path}'...")

    total_lines = 0
    kept_count = 0

    with open(input_path, "r", encoding="utf-8") as infile, open(
        output_path, "w", encoding="utf-8"
    ) as outfile:

        for line in infile:
            total_lines += 1
            stripped = line.strip()

            # 1. Skip lines that contain only spaces/tabs/newlines
            if not stripped:
                continue

            # 2. Collapse internal giant space gaps (e.g. 50 spaces -> 1 space)
            # This turns: "1     EN26...   NAME       OBC" into "1 EN26... NAME OBC"
            clean_line = re.sub(r"[ \t]+", " ", stripped)

            outfile.write(clean_line + "\n")
            kept_count += 1

    elapsed = time.time() - start
    print(f"[✓] Completed in {elapsed:.2f} seconds!")
    print(
        f"[✓] Processed {total_lines:,} raw lines -> Kept {kept_count:,} continuous records."
    )
    print(f"[✓] Packed file saved to: '{output_path}'")


if __name__ == "__main__":
    compress_to_continuous(INPUT_FILE, OUTPUT_FILE)

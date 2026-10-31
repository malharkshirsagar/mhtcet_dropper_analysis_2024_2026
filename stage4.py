import re
import time

INPUT_FILE = "stage3.txt"  # Change to your current filename if different
OUTPUT_FILE = "stage4.txt"

# Target header text block to delete
TARGET_BLOCK = """
                                                                                                                                               A.Y. 2023-24
                                                                                                                                                                                                       HSC /
                                                                                                                                                Minority              MHT-CET    MHT-CET     MHT-CET               HSC    HSC                               SSC     SSC
   Merit   Application                                                            PWD /                                        Percentile                                                                  Diploma  SSC Total   SSC
                                    Candidate's Full Name             Merit Exam     Category      Gender          EWS  TFWS Orphan   Type                 Math        Physics      Chemistry   HSC PCM %  Math  Physics                               Science  English
   No        ID                                                                                           Def                                  /Mark                                                                               / D.Voc.   %    Math %
                                                                                                                        (LM/RM)                  Percentile     Percentile     Percentile            %    %                      %     %
                                                                                                                                                                                                                                                               Total %"""


def remove_exact_header_block(infile: str, outfile: str):
    start = time.time()
    print(f"[*] Reading '{infile}'...")

    with open(infile, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize target block into a regex pattern that matches any whitespace/newlines
    tokens = TARGET_BLOCK.strip().split()
    pattern_str = r"\s*".join(re.escape(t) for t in tokens)
    header_regex = re.compile(pattern_str, re.IGNORECASE)

    print("[*] Stripping target header block across the entire file...")
    cleaned_content, count = header_regex.subn("", content)

    print(f"[*] Writing cleaned output to '{outfile}'...")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

    print(
        f"[✓] Done in {time.time() - start:.2f}s! Removed {count:,} occurrences of the header block."
    )


if __name__ == "__main__":
    remove_exact_header_block(INPUT_FILE, OUTPUT_FILE)

import time

INPUT_TXT = "stage5.txt"
OUTPUT_TXT = "stage6.txt"

HEADER_BLOCK = """Merit No,
Application ID,
Candidate's Full Name, 
Category, 
Gender, 
PWD / Def,
EWS,
TFWS, 
Orphan,
Minority Type (LM/RM),
Merit Exam,
Percentile /Mark,
MHT-CET-PCM Math Percentile,
MHT-CET-PCM Physics Percentile,
MHT-CET-PCM Chemistry Percentile,
HSC PCM %,
HSC Math %,
HSC Physics %,
HSC / Diploma / D.Voc.Total %,
SSC Total %,
SSC Math %,
SSC Science %,
SSC English %
"""


def prepend_header(source_path: str, dest_path: str):
    start = time.time()
    print(f"[*] Prepending header block to '{source_path}'...")

    with open(dest_path, "w", encoding="utf-8") as outfile:
        # 1. Write the multi-line header at line 1
        outfile.write(HEADER_BLOCK)

        # 2. Stream the continuous records right after
        with open(source_path, "r", encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)

    elapsed = time.time() - start
    print(f"[✓] Finished in {elapsed:.2f} seconds!")
    print(f"[✓] File ready: '{dest_path}'")


if __name__ == "__main__":
    prepend_header(INPUT_TXT, OUTPUT_TXT)

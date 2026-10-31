import csv

INPUT_TXT = "stage6.txt"
OUTPUT_CSV = "final_mht_cet_merit_high_precision.csv"


def generate_precise_csv(input_path: str, output_path: str):
    print(f"[*] Reading '{input_path}' and locking in 7-decimal string precision...")

    headers = [
        "Merit No",
        "Application ID",
        "Candidate's Full Name",
        "Category",
        "Gender",
        "Merit Exam",
        "Percentile / Mark",
        "MHT-CET-PCM Math Percentile",
        "MHT-CET-PCM Physics Percentile",
        "MHT-CET-PCM Chemistry Percentile",
        "HSC PCM %",
        "HSC Math %",
        "HSC Physics %",
        "HSC / Diploma / D.Voc. Total %",
        "SSC Total %",
        "SSC Math %",
        "SSC Science %",
        "SSC English %",
    ]

    rows_written = 0
    skipped = 0

    with open(input_path, "r", encoding="utf-8") as infile, open(
        output_path, "w", newline="", encoding="utf-8"
    ) as outfile:

        writer = csv.writer(outfile)
        writer.writerow(headers)

        for line in infile:
            line_str = line.strip()

            # Skip header repeats, page markers, or empty lines
            if (
                not line_str
                or "--- PAGE" in line_str
                or "Merit" in line_str
                or "Application" in line_str
            ):
                continue

            if "MHT-CET-PCM" not in line_str:
                skipped += 1
                continue

            # Split line into Left side and Right side at the exam keyword
            left_raw, right_raw = line_str.split("MHT-CET-PCM", 1)

            # --- 1. LEFT SIDE PROCESSING ---
            # Strip certificate receipt symbols ($@#) to clean up category tokens
            cleaned_left = left_raw.replace("$", "").replace("@", "").replace("#", "")
            tokens = cleaned_left.strip().split()

            if len(tokens) < 4:
                skipped += 1
                continue

            merit_no = tokens[0]
            app_id = tokens[1]

            # Locate Gender from the right side of the left token block
            gender_idx = -1
            gender = ""
            for i in range(len(tokens) - 1, 1, -1):
                if tokens[i].lower() in ["male", "female", "transgender"]:
                    gender_idx = i
                    gender = tokens[i]
                    break

            if gender_idx == -1:
                skipped += 1
                continue

            # Category is the token immediately preceding Gender
            category = tokens[gender_idx - 1]

            # Handle multi-word category prefixes (e.g., NT-C, VJ, etc.) if applicable
            if gender_idx >= 3 and tokens[gender_idx - 2].upper() in {
                "NT",
                "VJ",
                "SBC",
                "DT",
            }:
                category = f"{tokens[gender_idx - 2]} {category}"
                cat_offset = 2
            else:
                cat_offset = 1

            # Candidate's Full Name: strictly everything between App ID and Category
            name_tokens = tokens[2 : gender_idx - cat_offset]
            name = " ".join(name_tokens)

            # --- 2. RIGHT SIDE PROCESSING (PRECISION LOCKED) ---
            merit_exam = "MHT-CET-PCM"

            # Extract score tokens. DO NOT convert them to float() or int()
            # so trailing zeros (e.g., 100.0000000) are strictly preserved as strings.
            score_tokens = right_raw.strip().split()

            # Ensure exactly 12 score columns are maintained
            if len(score_tokens) < 12:
                score_tokens += [""] * (12 - len(score_tokens))
            elif len(score_tokens) > 12:
                score_tokens = score_tokens[:12]

            # --- 3. WRITE ROW DIRECTLY ---
            row = [merit_no, app_id, name, category, gender, merit_exam] + score_tokens

            writer.writerow(row)
            rows_written += 1

    print(
        f"\n[✓] Successfully processed and wrote {rows_written:,} high-precision records!"
    )
    print(f"[✓] Skipped rows: {skipped}")
    print(f"[✓] Final CSV saved to: '{output_path}'")


if __name__ == "__main__":
    generate_precise_csv(INPUT_TXT, OUTPUT_CSV)

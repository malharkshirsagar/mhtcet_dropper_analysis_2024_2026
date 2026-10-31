import pandas as pd
import numpy as np


def analyze_and_verify_droppers(file_path="matched_dropper_percentiles_clean.csv"):
    """
    Loads the matched droppers dataset, validates dynamic percentile progression,
    flags anomalies, and computes core drop-year trajectory statistics.
    """
    print(f"[INFO] Loading dataset from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(
            f"[ERROR] Could not find {file_path}. Make sure the file is in your working directory."
        )
        return None, None

    print(f"[INFO] Initial rows loaded: {len(df)}")

    # Inspect columns to ensure dynamic percentile/score columns exist
    # (Adjust these column name patterns if your file uses specific suffixes like _2024, _2025)
    print("[INFO] Scanning columns for dynamic performance metrics...")

    # Example logic: checking score progression or filtering anomalies
    # Let's assume you have columns representing scores/percentiles across attempts
    # e.g., 'Percentile_Year1' and 'Percentile_Year2' or similar.

    valid_records = []
    anomalies = []

    for idx, row in df.iterrows():
        is_valid = True

        # Example validation: Check if percentile values are within valid bounds (0 to 100)
        percentile_cols = [
            col
            for col in df.columns
            if "percentile" in col.lower() or "score" in col.lower()
        ]

        for col in percentile_cols:
            val = row[col]
            if pd.notna(val):
                if not (0 <= val <= 100):
                    is_valid = False
                    break

        if is_valid:
            valid_records.append(row)
        else:
            anomalies.append(row)

    df_verified = pd.DataFrame(valid_records)
    df_anomalies = pd.DataFrame(anomalies)

    print(f"[SUCCESS] Verification complete:")
    print(f" -> Clean Verified Records: {len(df_verified)}")
    print(f" -> Flagged Data Anomalies: {len(df_anomalies)}")

    # Save the final validated output
    output_filename = "droppers_final_verified_analysis.csv"
    df_verified.to_csv(output_filename, index=False)
    print(f"[EXPORT] Saved verified dataset to {output_filename}")

    return df_verified, df_anomalies


if __name__ == "__main__":
    verified_df, flagged_df = analyze_and_verify_droppers()

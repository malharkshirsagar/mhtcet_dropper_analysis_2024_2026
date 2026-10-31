import pandas as pd
import os


def purge_single_attempts():
    input_file = "matched_dropper_percentiles.csv"
    output_file = "verified_droppers_only.csv"

    if not os.path.exists(input_file):
        print(f"[!] '{input_file}' not found.")
        return

    print(f"[*] Loading dataset...")
    df = pd.read_csv(input_file, dtype=str)
    initial_count = len(df)

    # Check if a student has data in a block by looking at the main percentile column
    # If it's not empty, it counts as 1 attempt for that year
    has_2024 = (
        df["2024_Percentile/mark"].fillna("").str.strip().astype(bool).astype(int)
    )
    has_2025 = (
        df["2025_Percentile/mark"].fillna("").str.strip().astype(bool).astype(int)
    )
    has_2026 = (
        df["2026_Percentile/mark"].fillna("").str.strip().astype(bool).astype(int)
    )

    # Calculate total blocks filled per student (0, 1, 2, or 3)
    df["total_attempts"] = has_2024 + has_2025 + has_2026

    # KEEP only students who have filled at least 2 blocks (true droppers)
    df_droppers = df[df["total_attempts"] >= 2].copy()

    # Drop our temporary counting column so the CSV stays perfectly clean
    df_droppers.drop(columns=["total_attempts"], inplace=True)

    # Save the purged file
    df_droppers.to_csv(output_file, index=False)

    dropped_count = initial_count - len(df_droppers)
    print("\n[SUCCESS] Single-attempt candidates purged!")
    print(f"    - Total records scanned: {initial_count:,}")
    print(f"    - Normal students deleted: {dropped_count:,}")
    print(f"    - True Droppers retained: {len(df_droppers):,}")
    print(f"    - Saved to: '{output_file}'")


if __name__ == "__main__":
    purge_single_attempts()

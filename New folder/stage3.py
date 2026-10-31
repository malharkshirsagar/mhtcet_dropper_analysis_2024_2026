import pandas as pd
import os


def direct_attach_ssc():
    split_file = "stage2.csv"
    output_file = "stage3.csv"

    if not os.path.exists(split_file):
        raise FileNotFoundError(
            f"[!] '{split_file}' not found. Run your stage 2 split script first."
        )

    print(f"[*] Loading '{split_file}'...")
    df_master = pd.read_csv(split_file, dtype=str)
    df_master.columns = df_master.columns.str.strip()

    # Yearly source files mapping in exact order of stacking (2024 -> 2025 -> 2026)
    yearly_files = [
        ("2024", "2024.csv"),
        ("2025", "2025.csv"),
        ("2026", "2026.csv"),
    ]

    ssc_frames = []

    for year, filepath in yearly_files:
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"[!] Source file for {year} not found: '{filepath}'."
            )

        print(f"[*] Reading SSC columns from {filepath} ({year})...")
        df_yr = pd.read_csv(filepath, dtype=str)
        df_yr.columns = df_yr.columns.str.strip()

        # Dynamically locate SSC columns
        ssc_total = next(
            (c for c in df_yr.columns if "SSC" in c.upper() and "TOTAL" in c.upper()),
            None,
        )
        ssc_math = next(
            (c for c in df_yr.columns if "SSC" in c.upper() and "MATH" in c.upper()),
            None,
        )
        ssc_science = next(
            (c for c in df_yr.columns if "SSC" in c.upper() and "SCIENCE" in c.upper()),
            None,
        )
        ssc_english = next(
            (c for c in df_yr.columns if "SSC" in c.upper() and "ENGLISH" in c.upper()),
            None,
        )

        if not all([ssc_total, ssc_math, ssc_science, ssc_english]):
            raise ValueError(
                f"Could not locate all SSC columns in {filepath}. Found: {list(df_yr.columns)}"
            )

        df_ssc_yr = pd.DataFrame(
            {
                "SSC Total %": df_yr[ssc_total].fillna(""),
                "SSC Math %": df_yr[ssc_math].fillna(""),
                "SSC Science %": df_yr[ssc_science].fillna(""),
                "SSC English %": df_yr[ssc_english].fillna(""),
            }
        )
        ssc_frames.append(df_ssc_yr)

    # Concatenate all SSC frames vertically in exact year order
    print("[*] Concatenating SSC columns sequentially to match master rows...")
    df_all_ssc = pd.concat(ssc_frames, ignore_index=True)

    # Sanity check row count match
    if len(df_master) != len(df_all_ssc):
        raise ValueError(
            f"Row count mismatch! Master rows: {len(df_master):,}, SSC rows: {len(df_all_ssc):,}"
        )

    # Directly attach horizontally next to gender
    df_complete = pd.concat([df_master, df_all_ssc], axis=1)

    # Final column ordering check
    desired_order = [
        "exam year",
        "candidate full name",
        "surname",
        "candidate name",
        "father/mother name",
        "category",
        "gender",
        "SSC Total %",
        "SSC Math %",
        "SSC Science %",
        "SSC English %",
    ]

    existing_cols = [c for c in desired_order if c in df_complete.columns]
    other_cols = [c for c in df_complete.columns if c not in existing_cols]

    df_complete = df_complete[existing_cols + other_cols]

    # Export final complete dataset
    df_complete.to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Successfully attached SSC columns directly!")
    print(f"    - Saved to: '{output_file}'")
    print(f"    - Total records: {len(df_complete):,}")
    print(f"    - Final columns: {list(df_complete.columns)}")


if __name__ == "__main__":
    direct_attach_ssc()

import pandas as pd
import os


def attach_hsc_data():
    complete_file = "stage3.csv"
    output_file = "stage4.csv"

    if not os.path.exists(complete_file):
        raise FileNotFoundError(
            f"[!] '{complete_file}' not found. Run direct_attach_ssc.py first."
        )

    print(f"[*] Loading '{complete_file}'...")
    df_master = pd.read_csv(complete_file, dtype=str)
    df_master.columns = df_master.columns.str.strip()

    yearly_files = [("2024", "2024.csv"), ("2025", "2025.csv"), ("2026", "2026.csv")]

    hsc_frames = []

    for year, filepath in yearly_files:
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"[!] Source file for {year} not found: '{filepath}'."
            )

        print(f"[*] Reading HSC columns from {filepath} ({year})...")
        df_yr = pd.read_csv(filepath, dtype=str)
        df_yr.columns = df_yr.columns.str.strip()

        # Dynamically locate HSC / Diploma columns
        hsc_pcm = next(
            (c for c in df_yr.columns if "HSC" in c.upper() and "PCM" in c.upper()),
            None,
        )
        hsc_math = next(
            (c for c in df_yr.columns if "HSC" in c.upper() and "MATH" in c.upper()),
            None,
        )
        hsc_phy = next(
            (c for c in df_yr.columns if "HSC" in c.upper() and "PHYSICS" in c.upper()),
            None,
        )
        hsc_total = next(
            (
                c
                for c in df_yr.columns
                if ("HSC" in c.upper() or "DIP" in c.upper() or "D.VOC" in c.upper())
                and "TOTAL" in c.upper()
            ),
            None,
        )

        # Fallbacks if exact naming varies slightly
        if not hsc_pcm:
            hsc_pcm = next((c for c in df_yr.columns if "PCM" in c.upper()), "")
        if not hsc_math:
            hsc_math = next(
                (
                    c
                    for c in df_yr.columns
                    if "MATH" in c.upper() and "HSC" in c.upper()
                ),
                "",
            )
        if not hsc_phy:
            hsc_phy = next((c for c in df_yr.columns if "PHYSICS" in c.upper()), "")
        if not hsc_total:
            hsc_total = next(
                (
                    c
                    for c in df_yr.columns
                    if "TOTAL" in c.upper() and c != "SSC Total %"
                ),
                "",
            )

        df_hsc_yr = pd.DataFrame(
            {
                "HSC PCM %": (
                    df_yr[hsc_pcm].fillna("") if hsc_pcm in df_yr.columns else ""
                ),
                "HSC Math %": (
                    df_yr[hsc_math].fillna("") if hsc_math in df_yr.columns else ""
                ),
                "HSC Physics %": (
                    df_yr[hsc_phy].fillna("") if hsc_phy in df_yr.columns else ""
                ),
                "HSC / Diploma / D.Voc. Total %": (
                    df_yr[hsc_total].fillna("") if hsc_total in df_yr.columns else ""
                ),
            }
        )
        hsc_frames.append(df_hsc_yr)

    print("[*] Concatenating HSC columns sequentially to match master rows...")
    df_all_hsc = pd.concat(hsc_frames, ignore_index=True)

    if len(df_master) != len(df_all_hsc):
        raise ValueError(
            f"Row count mismatch! Master rows: {len(df_master):,}, HSC rows: {len(df_all_hsc):,}"
        )

    # Directly attach horizontally
    df_complete = pd.concat([df_master, df_all_hsc], axis=1)

    # Desired full column order
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
        "HSC PCM %",
        "HSC Math %",
        "HSC Physics %",
        "HSC / Diploma / D.Voc. Total %",
    ]

    existing_cols = [c for c in desired_order if c in df_complete.columns]
    other_cols = [c for c in df_complete.columns if c not in existing_cols]

    df_final = df_complete[existing_cols + other_cols]

    df_final.to_csv(output_file, index=False)
    print(f"[SUCCESS] Attached HSC columns successfully! Saved to '{output_file}'")
    print(f"    - Final columns: {list(df_final.columns)}")


if __name__ == "__main__":
    attach_hsc_data()

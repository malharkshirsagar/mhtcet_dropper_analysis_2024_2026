import pandas as pd
import os
import re


def normalize_name(full_name):
    """Tokenizes and alphabetizes names to neutralize formatting mismatches."""
    if pd.isna(full_name):
        return ""
    tokens = re.findall(r"[A-Z]+", str(full_name).upper())
    return "_".join(sorted(tokens))


def build_final_dropper_csv():
    # 1. Load your existing combined base CSV
    base_file = "stage4.csv"
    if not os.path.exists(base_file):
        print(
            f"[!] Base file '{base_file}' not found. Please ensure it's in the directory."
        )
        return

    print(f"[*] Loading base academic/demographic master...")
    df_base = pd.read_csv(base_file, dtype=str)
    df_base.columns = df_base.columns.str.strip()

    # Define our matching fingerprint: Normalized Name + SSC Total %
    name_col_base = next(
        (
            c
            for c in df_base.columns
            if "NAME" in c.upper() and "CANDIDATE" in c.upper()
        ),
        "candidate full name",
    )
    df_base["student full name"] = df_base[name_col_base].fillna("")
    df_base["Normalized_Name"] = df_base["student full name"].apply(normalize_name)
    df_base["Match_Key"] = (
        df_base["Normalized_Name"] + "_" + df_base["SSC Total %"].fillna("")
    )

    # 2. Map and index the raw yearly CSVs
    years = ["2024", "2025", "2026"]
    files = {"2024": "2024.csv", "2025": "2025.csv", "2026": "2026.csv"}

    yearly_lookups = {}
    for yr in years:
        if not os.path.exists(files[yr]):
            print(
                f"[!] Warning: Raw file '{files[yr]}' not found. Skipping {yr} scores."
            )
            continue

        print(f"[*] Indexing {yr} raw data for matching...")
        df_yr = pd.read_csv(files[yr], dtype=str)
        df_yr.columns = df_yr.columns.str.strip()

        name_col_yr = next(
            (c for c in df_yr.columns if "NAME" in c.upper()), "Candidate Full Name"
        )
        df_yr["Normalized_Name"] = df_yr[name_col_yr].fillna("").apply(normalize_name)
        ssc_total_yr = next(
            (c for c in df_yr.columns if "SSC" in c.upper() and "TOTAL" in c.upper()),
            "SSC Total %",
        )
        df_yr["Match_Key"] = (
            df_yr["Normalized_Name"] + "_" + df_yr[ssc_total_yr].fillna("")
        )

        # Locate percentile columns flexibly in the raw data
        pct_mark = next(
            (
                c
                for c in df_yr.columns
                if "PERCENTILE" in c.upper()
                and "MARK" in c.upper()
                or "PERCENTILE/MARK" in c.upper()
            ),
            None,
        )
        pct_math = next(
            (
                c
                for c in df_yr.columns
                if "MATH" in c.upper() and "PERCENTILE" in c.upper()
            ),
            None,
        )
        pct_phy = next(
            (
                c
                for c in df_yr.columns
                if "PHYSICS" in c.upper() and "PERCENTILE" in c.upper()
            ),
            None,
        )
        pct_chem = next(
            (
                c
                for c in df_yr.columns
                if "CHEMISTRY" in c.upper() and "PERCENTILE" in c.upper()
            ),
            None,
        )

        df_yr_indexed = df_yr.set_index("Match_Key")

        # Build dictionary for instant lookup by Match_Key
        lookup_dict = {}
        for idx, row in df_yr_indexed.iterrows():
            lookup_dict[idx] = {
                f"{yr}_Percentile/mark": row[pct_mark] if pct_mark in row.index else "",
                f"{yr}_MHT-CET-PCM Math Percentile": (
                    row[pct_math] if pct_math in row.index else ""
                ),
                f"{yr}_MHT-CET-PCM Physics Percentile": (
                    row[pct_phy] if pct_phy in row.index else ""
                ),
                f"{yr}_MHT-CET-PCM Chemistry Percentile": (
                    row[pct_chem] if pct_chem in row.index else ""
                ),
            }
        yearly_lookups[yr] = lookup_dict

    # 3. Iterate over the base rows and construct the final output
    print("[*] Matching rows and extracting yearly percentiles...")
    final_rows = []

    for _, row in df_base.iterrows():
        match_key = row["Match_Key"]

        new_row = {
            "student full name": row.get("student full name", ""),
            "category": row.get("category", ""),
            "gender": row.get("gender", ""),
            "SSC Total %": row.get("SSC Total %", ""),
            "SSC Math %": row.get("SSC Math %", ""),
            "SSC Science %": row.get("SSC Science %", ""),
            "SSC English %": row.get("SSC English %", ""),
            "HSC PCM %": row.get("HSC PCM %", ""),
            "HSC Math %": row.get("HSC Math %", ""),
            "HSC Physics %": row.get("HSC Physics %", ""),
            "HSC / Diploma / D.Voc. Total %": row.get(
                "HSC / Diploma / D.Voc. Total %", ""
            ),
        }

        # Look up 2024, 2025, and 2026 percentiles
        for yr in ["2024", "2025", "2026"]:
            if yr in yearly_lookups and match_key in yearly_lookups[yr]:
                new_row.update(yearly_lookups[yr][match_key])
            else:
                new_row.update(
                    {
                        f"{yr}_Percentile/mark": "",
                        f"{yr}_MHT-CET-PCM Math Percentile": "",
                        f"{yr}_MHT-CET-PCM Physics Percentile": "",
                        f"{yr}_MHT-CET-PCM Chemistry Percentile": "",
                    }
                )

        final_rows.append(new_row)

    df_final = pd.DataFrame(final_rows)

    # 4. Strict Enforcement of Requested Column Order
    target_columns = [
        "student full name",
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
        "2024_Percentile/mark",
        "2024_MHT-CET-PCM Math Percentile",
        "2024_MHT-CET-PCM Physics Percentile",
        "2024_MHT-CET-PCM Chemistry Percentile",
        "2025_Percentile/mark",
        "2025_MHT-CET-PCM Math Percentile",
        "2025_MHT-CET-PCM Physics Percentile",
        "2025_MHT-CET-PCM Chemistry Percentile",
        "2026_Percentile/mark",
        "2026_MHT-CET-PCM Math Percentile",
        "2026_MHT-CET-PCM Physics Percentile",
        "2026_MHT-CET-PCM Chemistry Percentile",
    ]

    for col in target_columns:
        if col not in df_final.columns:
            df_final[col] = ""

    df_final = df_final[target_columns]

    output_filename = "matched_dropper_percentiles.csv"
    df_final.to_csv(output_filename, index=False)

    print(f"\n[SUCCESS] Custom Row Matching Complete!")
    print(f"    - Saved exact requested format to '{output_filename}'")


if __name__ == "__main__":
    build_final_dropper_csv()

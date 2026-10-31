import pandas as pd
import os


def extract_and_tag_year(filepath, year):
    if not os.path.exists(filepath):
        print(f"[!] File not found: {filepath}. Skipping.")
        return None

    print(f"[*] Processing {year} from {filepath}...")
    df = pd.read_csv(filepath, dtype=str)
    df.columns = df.columns.str.strip()

    # Dynamically locate columns regardless of minor naming variations
    name_col = next((col for col in df.columns if "NAME" in col.upper()), None)
    cat_col = next((col for col in df.columns if "CATEGORY" in col.upper()), None)
    gender_col = next((col for col in df.columns if "GENDER" in col.upper()), None)

    if not name_col or not cat_col or not gender_col:
        raise ValueError(
            f"Could not find Name, Category, or Gender in {filepath}. Columns found: {list(df.columns)}"
        )

    # Create standardized subset
    subset = pd.DataFrame(
        {
            "exam year": year,
            "candidate full name": df[name_col],
            "category": df[cat_col],
            "gender": df[gender_col],
        }
    )

    print(f"    - Extracted {len(subset):,} records for {year}")
    return subset


if __name__ == "__main__":
    print("==================================================")
    print("   MULTI-YEAR DEMOGRAPHICS UNIFICATION PIPELINE   ")
    print("==================================================")

    # Define file mappings for the 3 years
    file_mappings = [
        (r"D:/MHTCET_DROPPER_PROJECT/New folder/2024.csv", "2024"),
        (r"D:/MHTCET_DROPPER_PROJECT/New folder/2025.csv", "2025"),
        (r"D:/MHTCET_DROPPER_PROJECT/New folder/2026.csv", "2026"),
    ]

    all_frames = []

    for filepath, year in file_mappings:
        df_year = extract_and_tag_year(filepath, year)
        if df_year is not None:
            all_frames.append(df_year)

    if all_frames:
        # Concatenate all years into one master DataFrame
        master_df = pd.concat(all_frames, ignore_index=True)

        # Export to single master CSV
        output_filename = "all_years_demographics_master.csv"
        master_df.to_csv(output_filename, index=False)
        print(f"\n[SUCCESS] Master dataset compiled successfully!")
        print(f"    - Total records across all years: {len(master_df):,}")
        print(f"    - Saved to: '{output_filename}'")
    else:
        print("\n[!] No files were successfully processed.")

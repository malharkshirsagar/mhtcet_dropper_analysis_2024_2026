import pandas as pd
import os


def split_name(full_name):
    """
    Splits candidate full name into (surname, candidate name, father/mother name)
    assuming standard MHT-CET format: SURNAME FIRSTNAME FATHERNAME.
    """
    if pd.isna(full_name):
        return "", "", ""
    tokens = str(full_name).strip().split()
    if len(tokens) == 0:
        return "", "", ""
    elif len(tokens) == 1:
        return tokens[0], "", ""
    elif len(tokens) == 2:
        return tokens[0], tokens[1], ""
    elif len(tokens) == 3:
        return tokens[0], tokens[1], tokens[2]
    else:
        # 4 or more tokens: Surname is first, Father/Mother is last, rest is candidate name
        surname = tokens[0]
        father_mother = tokens[-1]
        candidate_name = " ".join(tokens[1:-1])
        return surname, candidate_name, father_mother


def process_demographics():
    input_file = "stage1.csv"
    output_file = "stage2.csv"

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"[!] '{input_file}' not found in the current directory."
        )

    print(f"[*] Reading '{input_file}'...")
    df = pd.read_csv(input_file, dtype=str)
    df.columns = df.columns.str.strip()

    # Ensure column naming consistency
    name_col = next(
        (
            col
            for col in df.columns
            if "NAME" in col.upper() and "CANDIDATE" in col.upper()
        ),
        "candidate full name",
    )
    if name_col not in df.columns:
        name_col = next((col for col in df.columns if "NAME" in col.upper()), None)

    print(
        "[*] Splitting candidate full names into Surname, Candidate Name, and Father/Mother Name..."
    )
    split_results = df[name_col].apply(split_name)

    df["surname"] = [res[0] for res in split_results]
    df["candidate name"] = [res[1] for res in split_results]
    df["father/mother name"] = [res[2] for res in split_results]

    # Reorder columns as requested:
    # exam year, candidate full name, surname, candidate name, father/mother name, category, gender
    desired_order = [
        "exam year",
        name_col,
        "surname",
        "candidate name",
        "father/mother name",
        "category",
        "gender",
    ]

    # Filter only existing columns to avoid key errors
    existing_cols = [c for c in desired_order if c in df.columns]
    remaining_cols = [c for c in df.columns if c not in existing_cols]

    df_final = df[existing_cols + remaining_cols]

    # Export to output CSV
    df_final.to_csv(output_file, index=False)
    print(f"[SUCCESS] Processed file saved successfully as '{output_file}'")
    print(f"    - Total records processed: {len(df_final):,}")


if __name__ == "__main__":
    process_demographics()

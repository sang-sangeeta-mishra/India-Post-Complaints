"""
India Post Customer Complaints
Author: Sangeeta Mishra
Date: 04-30-2026
"""

import pandas as pd

# ─────────────────────────────────────────────
# STEP 1: Load Raw Data
# ─────────────────────────────────────────────
df = pd.read_excel("C:/Users/soumy/OneDrive - lr.edu (1)/Sang_Code/India_ post/Raw_data.xlsx")

print("Raw Data Shape:", df.shape)
print("Raw Columns:", df.columns.tolist())
print(df.head(3))
df.rename(columns={
    "Date of complain": "date",
    "article":          "article_id",
    "Service Type":     "service_type_raw",
    "issue":            "issue_text",
    "issue_type":       "issue_type_raw"
}, inplace=True)

# Drop booking_date column (not needed for analysis)
if "booking_date" in df.columns:
    df.drop(columns=["booking_date"], inplace=True)

# Convert Excel Serial Date to Proper Date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Extract Article Prefix (First 2 Letters)
df["article_prefix"] = df["article_id"].str[:2]

prefix_to_category = {
    # Speed Post (E series)
    "EA": "Speed Post (E)", "EB": "Speed Post (E)", "EC": "Speed Post (E)",
    "ED": "Speed Post (E)", "EE": "Speed Post (E)", "EF": "Speed Post (E)",
    "EG": "Speed Post (E)", "EH": "Speed Post (E)", "EI": "Speed Post (E)",
    "EJ": "Speed Post (E)", "EK": "Speed Post (E)", "EL": "Speed Post (E)",
    "EM": "Speed Post (E)", "EN": "Speed Post (E)", "EO": "Speed Post (E)",
    "EP": "Speed Post (E)", "EQ": "Speed Post (E)", "ER": "Speed Post (E)",
    "ES": "Speed Post (E)", "ET": "Speed Post (E)", "EU": "Speed Post (E)",
    "EV": "Speed Post (E)", "EW": "Speed Post (E)", "EX": "Speed Post (E)",
    "EY": "Speed Post (E)", "EZ": "Speed Post (E)",

    # Bulk Speed Post (J series)
    "JA": "Bulk Speed Post (J)", "JB": "Bulk Speed Post (J)", "JC": "Bulk Speed Post (J)",
    "JD": "Bulk Speed Post (J)", "JE": "Bulk Speed Post (J)", "JF": "Bulk Speed Post (J)",
    "JG": "Bulk Speed Post (J)", "JH": "Bulk Speed Post (J)", "JI": "Bulk Speed Post (J)",
    "JJ": "Bulk Speed Post (J)", "JK": "Bulk Speed Post (J)", "JL": "Bulk Speed Post (J)",
    "JM": "Bulk Speed Post (J)", "JN": "Bulk Speed Post (J)", "JO": "Bulk Speed Post (J)",

    # COD Parcel (C series)
    "CA": "COD (C)", "CB": "COD (C)", "CC": "COD (C)", "CD": "COD (C)",
    "CE": "COD (C)", "CF": "COD (C)", "CG": "COD (C)", "CH": "COD (C)",
    "CI": "COD (C)", "CJ": "COD (C)", "CK": "COD (C)", "CL": "COD (C)",
    "CM": "COD (C)", "CN": "COD (C)", "CO": "COD (C)", "CP": "COD (C)",
    "CQ": "COD (C)", "CR": "COD (C)", "CS": "COD (C)", "CT": "COD (C)",
    "CU": "COD (C)", "CV": "COD (C)", "CW": "COD (C)", "CX": "COD (C)",
    "CY": "COD (C)", "CZ": "COD (C)",

    # Registered (R series)
    "RA": "Registered (R)", "RB": "Registered (R)", "RC": "Registered (R)",
    "RD": "Registered ®",   "RE": "Registered (R)", "RF": "Registered (R)",

    # Registered Parcel (U series)
    "UA": "Registered Parcel (U)", "UB": "Registered Parcel (U)",
    "UC": "Registered Parcel (U)", "UD": "Registered Parcel (U)",

    # Parcel (P series)
    "PA": "Parcel (P)", "PB": "Parcel (P)", "PC": "Parcel (P)",
    "PD": "Parcel (P)", "PP": "Parcel (P)",

    # Air Mail (A series)
    "AW": "Air Mail (A)", "AX": "Air Mail (A)", "AY": "Air Mail (A)",

    # Other (M series)
    "MA": "Other (M)", "MB": "Other (M)", "MC": "Other (M)",
    "MD": "Other (M)", "ME": "Other (M)", "MF": "Other (M)",
    "MG": "Other (M)", "MH": "Other (M)", "MI": "Other (M)",
    "MJ": "Other (M)", "MK": "Other (M)", "ML": "Other (M)",
    "MM": "Other (M)", "MN": "Other (M)", "MO": "Other (M)",
    "MP": "Other (M)",
}

df["article_category"] = df["article_prefix"].map(prefix_to_category).fillna("Other")

service_type_map = {
    "Speed Post":          "Speed Post",
    "Speed Post Parcel":   "Speed Post",
    "Speedpost":           "Speed Post",
    "COD Parcel":          "COD Parcel",
    "International Article": "International Article",
    "Ack. Regd. Article":  "Ack. Regd. Article",
    "Registered Letter":   "Registered Letter",
}

df["service_type"] = df["service_type_raw"].map(service_type_map).fillna(df["service_type_raw"])
df.drop(columns=["service_type_raw"], inplace=True)

issue_type_map = {
    "Delivery Delay":       "Delivery Delay",
    "Delivery Issue":       "Delivery Delay",
    "Service Delay":        "Delivery Delay",
    "Missing Item":         "Missing Item",
    "Fake Delivery Attempt":"Fake Delivery Attempt",
    "Tracking Issue":       "Tracking Issue",
    "Service Issue":        "Service Issue",
    "Damage/Loss":          "Damage/Loss",
    "Wrong Delivery":       "Wrong Delivery",
    "Address Issue":        "Wrong Delivery",
    "Follow-up":            "Other",
    "Other":                "Other",
}

df["issue_type"] = df["issue_type_raw"].map(issue_type_map).fillna("Other")
df.drop(columns=["issue_type_raw"], inplace=True)


df = df[[
    "date",
    "article_id",
    "article_prefix",
    "article_category",
    "service_type",
    "issue_text",
    "issue_type"
]]


print("\n✅ Cleaned Data Shape:", df.shape)
print("✅ Cleaned Columns:", df.columns.tolist())
print("\nSample:")
print(df.head(5))
print("\nIssue Type Distribution:")
print(df["issue_type"].value_counts())
print("\nService Type Distribution:")
print(df["service_type"].value_counts())


# Save Cleaned Data

df.to_excel("india_post_complaints_analysis.xlsx",
            sheet_name="Clean_Data",
            index=False)

print("\n✅ Cleaned file saved as: india_post_complaints_analysis.xlsx")


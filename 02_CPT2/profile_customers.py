"""CTP 2 - Exercise 1 STARTER: profile customers.csv with pandas.
Run from the 02_CTP2 folder:  python profile_customers_starter.py
Goal: measure at least 8 rules (2 per dimension) and copy the numbers into quality_scorecard_template.csv
"""
import pandas as pd

df = pd.read_csv("../shopfast-kit/data/customers.csv", dtype=str)   # dtype=str: keep the raw text (e.g. 01300)
n = len(df)
print("Rows:", n)
print(df.head())

# --- Completeness: how many empty values per column? ---
print("\nEmpty values per column:\n", df.isna().sum())

# --- Uniqueness: is customer_id unique? ---
print("\nDuplicated customer_id rows:", df["customer_id"].duplicated(keep=False).sum())

# TODO 1 (Uniqueness): normalise email (strip + lower case) and count people registered twice
df["email_norm"] = df["email"].str.strip().str.lower()
print("\nDuplicated normalized emails:", df["email_norm"].dropna().duplicated(keep=False).sum())
# TODO 2 (Validity): count emails that do not match the regex  ^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$   (hint: .str.match)
invalid_emails = (~df["email"].dropna().str.strip().str.match(r'^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$')).sum()
print("\nInvalid emails:", invalid_emails)
# TODO 3 (Consistency): list the distinct values of country with value_counts() - how many spellings for 4 countries?
print("\nDistinct country values:")
print(df["country"].value_counts())
print("Distinct country spellings:", df["country"].nunique())
# TODO 4 (Consistency): count signup_date values that are NOT in the format YYYY-MM-DD
print("Date that are in a wrong format:",(~df["signup_date"].dropna().str.match(r'^\d{4}-\d{2}-\d{2}$')).sum())
# TODO 5 (Validity): loyalty_tier values outside bronze / silver / gold / platinum
print("Wrong values for loyalty_tier",(~df["loyalty_tier"].dropna().isin(["bronze","silver","gold","platinum"])).sum())
# TODO 6 (Accuracy): birth dates in the future or before 1906 (convert the ISO ones with pd.to_datetime)
converted_date = pd.to_datetime(df["birth_date"], format="%Y-%m-%d", errors="coerce")
invalid_dob = ((converted_date < "1906-01-01") | (converted_date > pd.Timestamp.today())).sum()
print("\nImplausible birth dates (before 1906 or in the future):", invalid_dob)
# TODO 7 (Validity): French postal codes that do not have 5 digits
df["fr_country"] = df["country"].str.strip().str.lower().isin(["fr", "france", "fra"])
print("French postal codes without 5 digits: ", (~(df.loc[df["fr_country"],"postal_code"].dropna().str.len() == 5)).sum())
# Bonus: compute score_pct = 100 * (1 - failing_rows / n) for each rule
def report_score(rule_name, failing, total):
    score = 100 * (1 - failing / total)
    print(f"{rule_name:<35} | failing: {failing:<4} | total: {total:<4} | score: {score:.2f}%")

print("\n--- SUMMARY SCORECARD ---")
# Exemples des 2 règles de base + tes 7 TODO :
report_score("Completeness: email not empty", df["email"].isna().sum(), n)
report_score("Uniqueness: customer_id", df["customer_id"].duplicated(keep=False).sum(), n)
report_score("TODO 1 - Uniqueness: email", df["email_norm"].dropna().duplicated(keep=False).sum(), df["email"].notna().sum())
report_score("TODO 2 - Validity: email regex", (~df["email"].dropna().str.strip().str.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")).sum(), df["email"].notna().sum())
report_score("TODO 3 - Consistency: country ISO", (~df["country"].dropna().isin(["FR", "DE", "ES", "BE"])).sum(), df["country"].notna().sum())
report_score("TODO 4 - Consistency: signup_date", (~df["signup_date"].dropna().str.match(r"^\d{4}-\d{2}-\d{2}$")).sum(), df["signup_date"].notna().sum())
report_score("TODO 5 - Validity: loyalty_tier", (~df["loyalty_tier"].dropna().isin(["bronze", "silver", "gold", "platinum"])).sum(), df["loyalty_tier"].notna().sum())

dob = pd.to_datetime(df["birth_date"], format="%Y-%m-%d", errors="coerce")
report_score("TODO 6 - Accuracy: birth_date", ((dob < "1906-01-01") | (dob > pd.Timestamp.today())).sum(), dob.notna().sum())

fr_cp = df.loc[df["fr_country"], "postal_code"].dropna().str.strip()
report_score("TODO 7 - Validity: FR postal_code", (~(fr_cp.str.len() == 5)).sum(), len(fr_cp))
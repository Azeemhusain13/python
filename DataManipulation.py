import pandas as pd
import numpy as np

# File paths
test_plan_file = "test_plan.xlsx"     # Source of Test Plan
storys_file = "storys.xlsx"           # Source of Storys

# Step 1: Load both sheets
test_plan_df = pd.read_excel(test_plan_file, sheet_name='Test Plan')
storys_df = pd.read_excel(storys_file, sheet_name='Storys')

# Step 2: Build key -> linked issues and test count map
def build_key_linked_issues_map(test_plan_df):
    key_linked_issue_map = {}
    grouped = test_plan_df.groupby('key')

    for key, group in grouped:
        linked_issues = group['linked issue key'].dropna().tolist()
        test_count = group['Test Count'].iloc[0]  # assuming same count per key
        key_linked_issue_map[key] = {
            "linked_issues": linked_issues,
            "test_count": test_count
        }
    return key_linked_issue_map

key_linked_issue_mapping = build_key_linked_issues_map(test_plan_df)

# Step 3: Build Storys key -> time mapping
storys_time_map = {}

for _, row in storys_df.iterrows():
    story_key = str(row['key']).strip()
    time_seconds = row['Time']
    if pd.isna(time_seconds):
        time_seconds = 0
    storys_time_map[story_key] = time_seconds

# Step 4: Calculate total hours
final_result = []

for main_key, data in key_linked_issue_mapping.items():
    linked_issues = data['linked_issues']
    test_count = data['test_count']

    total_seconds = sum(
        storys_time_map.get(linked_key, 0) or 0
        for linked_key in linked_issues
    )
    total_hours = total_seconds / 3600

    final_result.append({
        "Key": main_key,
        "Linked Issues": ', '.join(linked_issues),
        "Test Count": test_count,
        "Total Hours": round(total_hours, 2)
    })

# Step 5: Save into a new sheet in test_plan.xlsx
final_df = pd.DataFrame(final_result)

with pd.ExcelWriter(test_plan_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    final_df.to_excel(writer, sheet_name='Final Result', index=False)

import json
import csv

# Load the JSON file
json_file_path = "The_Gauntlet_Returns.json"
csv_file_path = "The_Gauntlet_Returns.csv"

with open(json_file_path, "r", encoding="utf-8") as file:
    data_pages = json.load(file)

# Define CSV headers based on expected structure
csv_headers = [
    "user_id", "entry_id", "draft_id", "status", "contest_style", "entry_count", 
    "pick_id", "appearance_id", "pick_number", "points"
]

# Extract data and format it for CSV
csv_rows = []

draft_id = ""
draft_status = ""
draft_contest_style = ""
draft_entry_count = ""

all_draft_entries = []
all_picks = []

for page in data_pages:
    draft = page.get("draft", {})
    draft_entries = page.get("draft_entries", [])
    picks = page.get("picks", [])
    
    # Store draft metadata only once
    if not draft_id:
        draft_id = draft.get("id", "")
        draft_status = draft.get("status", "")
        draft_contest_style = draft.get("contest_style_id", "")
        draft_entry_count = draft.get("entry_count", "")
    
    all_draft_entries.extend(draft_entries)
    all_picks.extend(picks)

# Create a mapping of picks by entry_id
picks_by_entry = {}
for pick in all_picks:
    entry_id = pick.get("draft_entry_id", "")
    if entry_id:
        if entry_id not in picks_by_entry:
            picks_by_entry[entry_id] = []
        picks_by_entry[entry_id].append(pick)

# Process each draft entry and associate it with its picks
for entry in all_draft_entries:
    user_id = entry.get("user_id", "")
    entry_id = entry.get("id", "")
    
    entry_picks = picks_by_entry.get(entry_id, [])
    
    for pick in entry_picks:
        csv_rows.append([
            user_id,
            entry_id,
            draft_id,
            draft_status,
            draft_contest_style,
            draft_entry_count,
            pick.get("id", ""),
            pick.get("appearance_id", ""),
            pick.get("number", ""),
            pick.get("points", "")
        ])

# Write data to CSV
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_headers)
    writer.writerows(csv_rows)

print(f"CSV file created: {csv_file_path}")

import json
import csv
import os

# Get all JSON files in the current directory
json_files = [f for f in os.listdir() if f.endswith(".json")]

for json_file in json_files:
    csv_file = json_file.replace(".json", ".csv")

    with open(json_file, "r", encoding="utf-8") as file:
        data_pages = json.load(file)

    # Define CSV headers
    csv_headers = [
        "user_id", "username", "entry_id", "draft_id", "status", "contest_style", "entry_count",
        "pick_1", "pick_2", "pick_3", "pick_4", "pick_5", "pick_6", "pick_7", "pick_8", "pick_9", "pick_10"
    ]

    # Extract data and format it for CSV
    csv_rows = []

    draft_id = ""
    draft_status = ""
    draft_contest_style = ""
    draft_entry_count = ""

    all_draft_entries = []
    all_picks = []
    user_map = {}

    for page in data_pages:
        draft = page.get("draft", {})
        draft_entries = page.get("draft_entries", [])
        picks = page.get("picks", [])
        users = page.get("users", [])

        # Store draft metadata only once
        if not draft_id:
            draft_id = draft.get("id", "")
            draft_status = draft.get("status", "")
            draft_contest_style = draft.get("contest_style_id", "")
            draft_entry_count = draft.get("entry_count", "")

        all_draft_entries.extend(draft_entries)
        all_picks.extend(picks)

        # Map user IDs to usernames
        for user in users:
            user_map[user.get("id", "")] = user.get("username", "")

    # Map picks to their respective entries
    picks_dict = {}
    for pick in all_picks:
        entry_id = pick.get("draft_entry_id", "")
        if entry_id not in picks_dict:
            picks_dict[entry_id] = []
        picks_dict[entry_id].append(pick.get("appearance_id", ""))

    # Ensure each entry has exactly 10 picks (pad with empty values if needed)
    for entry in all_draft_entries:
        user_id = entry.get("user_id", "")
        username = user_map.get(user_id, "")
        entry_id = entry.get("id", "")
        entry_picks = picks_dict.get(entry_id, [])[:10]  # Get first 10 picks if more exist
        entry_picks.extend([""] * (10 - len(entry_picks)))  # Pad if less than 10 picks

        csv_rows.append([
            user_id,
            username,
            entry_id,
            draft_id,
            draft_status,
            draft_contest_style,
            draft_entry_count,
            *entry_picks
        ])

    # Write data to CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_headers)
        writer.writerows(csv_rows)

    print(f"CSV file created: {csv_file}")

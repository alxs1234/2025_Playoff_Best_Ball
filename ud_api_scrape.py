import json
import requests
import re


auth_token = "YOUR_AUTH_TOKEN" # Find your UD Auth Token in chrome dev tools - network tab - Request Headers Authorization: and replace inside quotes. should be ~900 characters

draft_id = "DRAFT_ID_FOR_CONTEST" # Find Draft ID in chrome dev tools network tab, look for XHR request like this f3e70ddd-829b-4fab-8566-bc5e42580d15

base_url = f"https://api.underdogfantasy.com/v1/tournaments/drafts/{draft_id}"

headers = {
    "Authorization": f"Bearer {auth_token}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

all_data = []  # Store all fetched data
title_slug = "underdog_draft"  # Default in case title is missing

# Iterate through pages until we find no more data
page = 1
while True:
    url = f"{base_url}?page={page}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        break

    data = response.json()

    if data.get("meta", {}).get("items", 0) == 0:
        print(f"No data on page {page}, stopping.")
        break  # No more data available
    
    all_data.append(data)  # Store data
    
    # Extract title dynamically from first response
    if page == 1 and "draft" in data and "title" in data["draft"]:
        title_slug = re.sub(r"\s+", "_", data["draft"]["title"])  # Replace spaces with underscores

    page += 1  # Move to the next page

# Save collected data to a JSON file
if all_data:
    output_filename = f"{title_slug}.json"

    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, indent=4)

    print(f"Underdog data successfully saved to {output_filename}")

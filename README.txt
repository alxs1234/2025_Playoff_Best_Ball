I am running this on windows so if your a mac user you may need to make some changes but here are the instructions to get this to work for you.

Download Chrome Web Driver, unzip and place chromedriver.exe in C:\WebDriver\
https://googlechromelabs.github.io/chrome-for-testing/
win64 version - https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.159/win64/chromedriver-win64.zip


Instally Visual Studio Code
https://code.visualstudio.com/

Install Python inside Visual Studio Code - Extensions Tab
https://marketplace.visualstudio.com/items?itemName=ms-python.python

can also install Python Extension Pack (may not be necessary)
https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack


Once VS Code is setup with python in Explorer Tab Create ud_webscraping.py file in whatever folder you want to start it from i.e. C:\Users\{username}\{path_to_py_folder}\
and copy in my script

---

import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

# --- CONFIGURATION ---
USERNAME = "my username"  # Replace with your actual username/email
PASSWORD = "my password"  # Replace with your actual password
CHROME_DRIVER_PATH = r'C:\WebDriver\chromedriver.exe'
output_dir = r"C:\Users\{username}\Desktop\NFL\scrape"

# Ensure output directory exists
if not os.path.exists(output_dir):
    print(f"📂 Output directory not found. Creating: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

# --- GET CONTEST NUMBER FROM COMMAND LINE ---
try:
    contest_index = int(sys.argv[1]) - 1  # Convert input to zero-based index
    if contest_index < 0:
        raise ValueError
except (IndexError, ValueError):
    contest_index = 0  # Default to first contest if input is missing/invalid

print(f"🔄 Running script for Contest #{contest_index + 1}...")

# --- SET UP WEBDRIVER ---
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Navigate to the login page
driver.get("https://underdogfantasy.com/live/best-ball/nfl/")
time.sleep(5)  # Allow page to load

# --- LOGIN PROCESS ---
try:
    print("🔄 Attempting login...")
    email_field = driver.find_element(By.CSS_SELECTOR, '[data-testid="email_input"]')
    email_field.send_keys(USERNAME)

    password_field = driver.find_element(By.CSS_SELECTOR, '[data-testid="password_input"]')
    password_field.send_keys(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="sign-in-button"]')
    login_button.click()

    # Wait for contests to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "styles__draftPoolTournamentCell__t5vYo"))
    )
    print("✅ Login successful!")

except Exception as e:
    print(f"❌ Login failed: {e}")
    driver.quit()
    exit()

# --- FIND CONTEST TITLES BEFORE CLICKING ---
try:
    print("🔍 Looking for contest titles...")

    contest_titles = driver.find_elements(By.CLASS_NAME, "styles__draftPoolTitle__PBQL9")
    contests = driver.find_elements(By.CLASS_NAME, "styles__draftPoolTournamentCell__t5vYo")

    if contests and contest_titles:
        total_contests = len(contests)
        print(f"🎯 Found {total_contests} contests.")

        if contest_index >= total_contests:
            print(f"❌ Contest #{contest_index + 1} does not exist! Exiting...")
            driver.quit()
            exit()

        # Extract contest title
        contest_title = contest_titles[contest_index].text.strip()
        contest_title = contest_title.split(" -")[0]  # Remove extra text like "- Semifinals"
        contest_title = contest_title.replace(" ", "_").replace("/", "_")

        print(f"📌 Selected Contest Title: {contest_title}")

        # Click the selected contest
        print(f"🎯 Clicking Contest #{contest_index + 1}...")
        contests[contest_index].click()
        time.sleep(5)  # Ensure page loads

        print("🏆 Contest opened successfully!")

    else:
        print("❌ No contests found!")
        driver.quit()
        exit()

except Exception as e:
    print(f"❌ Error finding contest titles: {e}")
    driver.quit()
    exit()
    
# --- CLICK ON "MY TEAM" ---
try:
    teams = driver.find_elements(By.CLASS_NAME, "styles__draftListCell__QdGry")

    if teams:
        print("🎯 Found teams. Clicking on my team...")
        teams[0].click()  # Click the first team (My Team)

        # Wait for the leaderboard to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "styles__leaderboard__jo8jK"))
        )
        print("✅ My Team loaded successfully!")

    else:
        print("❌ No teams found!")
        driver.quit()
        exit()

except Exception as e:
    print(f"❌ Error selecting team: {e}")
    driver.quit()
    exit()

# --- LOAD ALL TEAMS FROM LEADERBOARD ---
try:
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'styles__buttonWrapper__L0OYC')]/button"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(2)
            print("🔄 Clicked Load More...")
        except:
            print("✅ All teams are now visible or button is gone!")
            break

    # Extract all team elements
    team_elements = driver.find_elements(By.CLASS_NAME, "styles__draftEntryLeaderboardCell__b5oph")

    team_data = []

    # Iterate through each team
    for i, team in enumerate(team_elements):
        try:
            print(f"🔍 Processing team {i + 1} of {len(team_elements)}...")

            # Click on team
            driver.execute_script("arguments[0].click();", team)
            time.sleep(2)  # Allow modal to load

            # Wait for modal to appear
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "styles__draftTeamModal__hp65U"))
            )

            # Extract username
            username = driver.find_element(By.CLASS_NAME, "styles__username__RCggG").text

            # Extract player data grouped by position
            player_data = []
            position_sections = driver.find_elements(By.CLASS_NAME, "styles__playerList__NkYqo")

            for section in position_sections:
                position_blocks = section.find_elements(By.XPATH, "./div")

                for block in position_blocks:
                    try:
                        # Extract position
                        position_header = block.find_element(By.CLASS_NAME, "styles__positionHeader__ZwoSE")
                        position = position_header.text.strip()

                        # Extract all players for this position
                        players = block.find_elements(By.CLASS_NAME, "styles__playerName__uf8z0")

                        for player in players:
                            player_name = player.text.strip()
                            player_team = player.find_element(By.XPATH, "./following-sibling::div/p/strong").text.strip()

                            # Append to list
                            player_data.append([username, position, player_name, player_team])

                    except Exception as e:
                        print(f"⚠️ Error extracting position header data: {e}")

            if player_data:
                team_data.extend(player_data)
            else:
                print(f"⚠️ Warning: No players found for team {username}.")

            # Close the modal (press ESC)
            driver.find_element(By.TAG_NAME, "body").send_keys("\uE00C")
            time.sleep(2)  # Ensure modal is closed before moving to next team

        except Exception as e:
            print(f"❌ Error processing team: {e}")
            continue  # Move to the next team even if an error occurs

    print(f"📊 Extracted {len(team_data)} player entries.")

    # --- SAVE TO CSV ---
    output_file = os.path.join(output_dir, f"{contest_title}.csv")
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Position', 'Player Name', 'Team'])
        writer.writerows(team_data)

    print(f"✅ Player rosters saved to: {output_file}")

except Exception as e:
    print(f"❌ Error processing teams: {e}")

# --- CLOSE BROWSER ---
driver.quit()

---

Next you will need to change a few lines of code so it will work on your machine

---
# --- CONFIGURATION ---
USERNAME = "my username"  # Replace with your actual username/email
PASSWORD = "my password"  # Replace with your actual password
CHROME_DRIVER_PATH = r'C:\WebDriver\chromedriver.exe' # Replace with your driver path
output_dir = r"C:\Users\{username}\Desktop\NFL\scrape" # Replace with your username

---


next install pip in the terminal
python -m pip install --upgrade pip

then run this to install the required dependencies
pip install selenium
if pip isn't found try and run
pip3 install selenium


now you should be able to start the script

in the terminal type

cd C:\Users\{username}\{path_to_py_folder}\

python ud_webscraping.py
or
python3 ud_webscraping.py

If you have multiple lobbies rerun the script with the number of the lobby after i.e. 1 or nothing for first lobby, 2 for second, etc 

python ud_webscraping.py 2
or
python3 ud_webscraping.py 2


Wait for the script to finish running and then you will have a csv with the contest name in the NFL\scrape\ folder set in the configuration path 

Please note the script will double your team to you will likely have to delete rows 2-11 when you process it as it is just reading every team visible right now

import json
import os
import sys
import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# ===== Funcție pentru a crea fișier JSON dacă lipsește =====
def ensure_file_exists(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        print(f"⚠️ Fișierul {filename} nu exista. A fost creat gol. Completează-l și rulează din nou.")
        sys.exit(1)

# ===== Creează fișierele dacă nu există =====
ensure_file_exists("config.json", {
    "league_url": "",
    "output_file": "NumeFisier.csv",
    "num_matches": 10
})
ensure_file_exists("teams.json", {"": ""})

# ===== Încarcă setările =====
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open("teams.json", "r", encoding="utf-8") as f:
    team_replacements = json.load(f)

league_url = config["league_url"]
output_file = config["output_file"]
num_matches = config.get("num_matches", 10)  # dacă nu e setat, default 10

# ===== Configurare WebDriver =====
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# ===== Navigare la pagina ligi =====
driver.get(league_url)
time.sleep(3)

# ===== Apasă „Arată mai multe meciuri” =====
while True:
    try:
        btn = driver.find_element(By.CSS_SELECTOR, "a.event__more.event__more--static")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)
    except (NoSuchElementException, ElementClickInterceptedException):
        break

# ===== Extrage link-urile ultimelor N meciuri =====
all_links = driver.find_elements(By.CSS_SELECTOR, "a.eventRowLink")
match_links = [m.get_attribute("href") for m in all_links[:num_matches]]

# ===== Funcție pentru extragerea valorilor statistice =====
def get_stat_value(stat_name, strip_percent=False):
    try:
        container = driver.find_element(By.XPATH, f"//div[div/strong[contains(text(), '{stat_name}')]]")
        value1 = container.find_element(By.XPATH, "./div[1]/strong").text
        value2 = container.find_element(By.XPATH, "./div[3]/strong").text
        if strip_percent:
            value1 = value1.replace('%','').strip()
            value2 = value2.replace('%','').strip()
        return value1, value2
    except:
        return "0", "0"

# ===== Deschide CSV și scrie header =====
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Team1","Team2","Score1","Score2","Corners1","Corners2","ShotsOnTarget1","ShotsOnTarget2",
        "Offsides1","Offsides2","YellowCards1","YellowCards2","Fouls1","Fouls2",
        "ThrowIns1","ThrowIns2","Possesion1","Possesion2","xG1","xG2"
    ])

    # ===== Procesare meciuri =====
    for index, match_url in enumerate(match_links):
        driver.get(match_url)
        time.sleep(1)
        try:
            team1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.participant__participantName"))).text
            team2 = driver.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].text
            team1 = team_replacements.get(team1, team1)
            team2 = team_replacements.get(team2, team2)

            score1 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='detailScore__wrapper']/span[1]"))).text
            score2 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='detailScore__wrapper']/span[3]"))).text

            stats_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'statistici-meci')]")))
            driver.execute_script("arguments[0].click();", stats_tab)
            time.sleep(0.5)

            corners1, corners2 = get_stat_value("Cornere")
            shots_on_target1, shots_on_target2 = get_stat_value("Șuturi pe poartă")
            offsides1, offsides2 = get_stat_value("Ofsaiduri")
            yellow_cards1, yellow_cards2 = get_stat_value("Cartonașe galbene")
            fouls1, fouls2 = get_stat_value("Faulturi")
            throw_ins1, throw_ins2 = get_stat_value("Aruncări de la margine")
            possesion1, possesion2 = get_stat_value("Posesie minge", strip_percent=True)
            xG1, xG2 = get_stat_value("Goluri așteptate (xG)")

            writer.writerow([
                team1, team2, score1, score2, corners1, corners2, shots_on_target1, shots_on_target2,
                offsides1, offsides2, yellow_cards1, yellow_cards2, fouls1, fouls2,
                throw_ins1, throw_ins2, possesion1, possesion2, xG1, xG2
            ])

            print(f"[{index+1}] {team1} {score1}-{score2} {team2} | Cornere: {corners1}-{corners2}")

        except Exception as e:
            print(f"Eroare la meciul {index+1}: {e}")

driver.quit()
print("✅ Finalizat! CSV creat cu succes!")

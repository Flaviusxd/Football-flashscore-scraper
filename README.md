# Football Flashscore Scraper ⚽

Acest proiect Python face web scraping pe [Flashscore](https://www.flashscore.ro) pentru a extrage statistici din meciurile de fotbal ale unei ligi. Datele sunt salvate într-un fișier CSV.

---

## Funcționalități

- Extrage link-urile ultimelor meciuri dintr-o ligă.
- Colectează date despre echipe, scor, cornere, șuturi pe poartă, ofsaiduri, cartonașe galbene, faulturi, aruncări de la margine, posesie și xG.
- Suport pentru înlocuirea numelor echipelor cu alias-uri printr-un fișier `teams.json`.
- Configurabil prin `config.json`:
  - URL-ul ligii
  - Numele fișierului CSV
  - Numărul de meciuri de extras

---

## Structura proiectului

flashscore-scraper/
│
├─ main.py # Scriptul principal
├─ config.json # Configurații (URL ligă, output CSV, nr. meciuri)
├─ teams.json # Dicționar de înlocuire echipe
├─ requirements.txt # Dependențe Python
└─ README.md # Acest fișier

---

## Instalare

1. Clonează repo-ul:

```bash
git clone https://github.com/Flaviusxd/Football-flashscore-scraper.git
cd flashscore-scraper

Creează un mediu virtual (recomandat):
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux / Mac

Instalează dependențele:
python -m pip install --upgrade pip
pip install -r requirements.txt

Configurare
Editează config.json
Editează teams.json pentru a adăuga alias-uri pentru echipe:
  {
    "Manchester City": "mcity",
    "Rapid București": "rapid"
  }

Utilizare
Rulează scriptul:
  python main.py
După finalizare, fișierul CSV va fi creat cu datele meciurilor.

Notă
  Acest proiect este doar pentru scopuri educaționale.
  Asigură-te că respecți termenii și condițiile site-ului Flashscore.

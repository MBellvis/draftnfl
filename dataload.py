import requests

url = "https://github.com/nflverse/nflverse-data/releases/download/draft_picks/draft_picks.csv"

print("📥 Descargando dataset...")

response = requests.get(url)

with open("data/prospects.csv", "wb") as f:
    f.write(response.content)

print("✅ Dataset descargado correctamente")
import pandas as pd

df = pd.read_csv("data/hoja1draft2026.csv", header=None)

data = df[0].dropna().tolist()

rows = []

i = 0
while i < len(data) - 3:
    
    value = str(data[i]).strip()

    valid_positions = [
    "QB","RB","WR","TE","OT","OL","IOL","G","OG","C",
    "EDGE","DL","DT","IDL","LB","ILB","OLB",
    "CB","S","DB"
]

# ✅ detectar bloque válido completo (no solo el rank)
    if (
        value.isdigit() and
        i + 3 < len(data) and
        str(data[i+2]).strip().upper() in valid_positions
    ):
        try:
            rank = int(value)

            name = str(data[i+1]).strip()
            position = str(data[i+2]).strip()
            college = str(data[i+3]).strip()
            
            position = position.upper()
            rows.append([rank, name, position, college])

            i += 4
        except:
            i += 1
    else:
        i += 1

clean_df = pd.DataFrame(rows, columns=["rank", "name", "position", "college"])

clean_df.to_csv("data/prospects_current.csv", index=False)

print("✅ CSV limpio generado")
print(clean_df.head())
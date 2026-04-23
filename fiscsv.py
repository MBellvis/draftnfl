import pandas as pd


df = pd.read_csv("data/hoja1draft2026.csv", header=None)

data = df[0].dropna().tolist()

rows = []

for i in range(0, len(data), 5):
    try:
        rank = data[i]
        name = data[i+1]
        position = data[i+2]
        college = data[i+3]
        # data[i+4] → lo ignoramos (pick/equipo)
        
        rows.append([rank, name, position, college])
    except:
        pass

clean_df = pd.DataFrame(rows, columns=["rank", "name", "position", "college"])

clean_df.to_csv("data/prospects_current.csv", index=False)

print("✅ CSV limpio generado")
print(clean_df.head())
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar datos
df = pd.read_csv("data/prospects.csv")
df.columns = df.columns.str.lower()

# 2. Seleccionar columnas
df = df[[
    "season",
    "round",
    "pick",
    "position",
    "team",
    "probowls",
    "allpro",
    "w_av"
]]

# 3. Filtrar últimos años
df = df[df["season"] >= 2010]

# 4. Crear métrica de éxito
df["success"] = (df["probowls"] > 0) | (df["allpro"] > 0)

# 5. TOP 10
top10 = df[df["pick"] <= 10]

# 📊 6. Picks por posición
pos_counts = top10["position"].value_counts()
print("📊 Picks por posición:\n")
print(pos_counts)

# 📈 7. Tasa de éxito
success = top10.groupby("position")["success"].mean()
print("\n📈 Tasa de éxito:\n")
print(success)

# 💥 8. VALOR MEDIO (AQUÍ)
value = top10.groupby("position")["w_av"].mean()
print("\n📊 Valor medio (Approximate Value):\n")
print(value)

# 📉 9. Gráfico (opcional)
pos_counts.plot(kind="bar")
plt.title("Top 10 Picks by Position (since 2010)")
plt.show()
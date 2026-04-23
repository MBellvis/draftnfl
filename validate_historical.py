import pandas as pd
from analyze_player import *

# =========================
# CONFIG
# =========================

YEAR = 2025

# =========================
# LOAD DATA
# =========================

df_hist = load_historical_data()

# 🔥 IMPORTANTE: NO perder nombres
if "pfr_player_name" in df_hist.columns:
    df_hist = df_hist.rename(columns={"pfr_player_name": "name"})

# fallback por si no existe
if "name" not in df_hist.columns:
    df_hist["name"] = "Unknown"

df_year = df_hist[df_hist["season"] == YEAR].copy()

results = []

# =========================
# MÉTRICAS CON STD
# =========================

def compute_metrics_with_std(df, pos, pick):
    comps = normalize_position(pos)
    low, high = get_pick_range(pick)

    df_range = df[(df["pick"] >= low) & (df["pick"] <= high)]
    df_pos = df_range[df_range["position"].isin(comps)]

    if df_pos.empty:
        return None, None, None

    return (
        df_pos["success"].mean(),
        df_pos["w_av"].mean(),
        df_pos["w_av"].std()
    )

# =========================
# VALIDACIÓN
# =========================

for _, row in df_year.iterrows():
    pick = row["pick"]
    pos = row["position"]

    # 🔥 nombre robusto (sin Unknown innecesario)
    name = row.get("name")
    if pd.isna(name) or name == "Unknown":
        name = f"{pos} #{pick}"

    #real_value = row["w_av"]
    real_value = row["w_av"] * 5  # 🔥 ajuste rookie → carrera

    success, expected_value, std = compute_metrics_with_std(df_hist, pos, pick)

    if expected_value is None or std is None or std < 1:
        continue        

    diff = real_value - expected_value
    z = diff / std

    results.append({
        "name": name,
        "pick": pick,
        "pos": pos,
        "real_value": real_value,
        "expected_value": round(expected_value, 2),
        "diff": round(diff, 2),
        "z_score": round(z, 2)
    })

df = pd.DataFrame(results)

# =========================
# CLASIFICACIÓN Z-SCORE
# =========================

def classify_result(z):
    if z > 1.5:
        return "🔥 STEAL"
    elif z > 0.5:
        return "👍 GOOD"
    elif z > -0.5:
        return "≈ EXPECTED"
    elif z > -1.5:
        return "⚠️ BAD"
    else:
        return "💥 BUST"

df["result"] = df["z_score"].apply(classify_result)

# =========================
# OUTPUT
# =========================

print(f"\n📊 VALIDACIÓN MODELO — DRAFT {YEAR}\n")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1400)

print(df.sort_values("pick").head(32))

# =========================
# MÉTRICAS
# =========================

print("\n📈 MÉTRICAS:\n")

print("Media diferencia:", round(df["diff"].mean(), 2))
print("Media z-score:", round(df["z_score"].mean(), 2))
print("Correlación:", round(df["real_value"].corr(df["expected_value"]), 2))

# =========================
# MEJORES PICKS
# =========================

print("\n🔥 MEJORES PICKS:\n")
print(df.sort_values("z_score", ascending=False).head(10)[
    ["name", "pick", "pos", "real_value", "expected_value", "z_score", "result"]
])

# =========================
# PEORES PICKS
# =========================

print("\n💥 PEORES PICKS:\n")
print(df.sort_values("z_score").head(10)[
    ["name", "pick", "pos", "real_value", "expected_value", "z_score", "result"]
])
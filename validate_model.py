import pandas as pd

# =========================
# CONFIG
# =========================

HISTORICAL_CSV = "data/prospects.csv"
CURRENT_BOARD_CSV = "data/big_board_2025.csv"

TEAM_NEEDS = {
    "Giants": {
        "HIGH": ["IOL", "OL", "DT", "DL", "CB"],
        "MEDIUM": ["LB", "WR", "S"],
        "LOW": ["OT", "EDGE", "RB", "TE", "QB"]
    }
}

POSITION_MAP = {
    "EDGE": ["DE", "OLB", "LB", "DL"],
    "OT": ["T", "OT", "OL"],
    "OL": ["OL", "T", "OT", "G", "OG", "C"],
    "IDL": ["DT", "DL"],
    "DT": ["DT", "DL"],
    "CB": ["CB", "DB"],
    "S": ["S", "DB"],
    "DB": ["CB", "S", "DB"],
    "LB": ["LB", "ILB", "OLB"],
    "WR": ["WR"],
    "QB": ["QB"],
    "RB": ["RB"],
    "TE": ["TE"]
}

POSITION_VALUE = {
    "HIGH": ["QB", "EDGE", "OT", "WR", "CB"],
    "MEDIUM": ["LB", "S", "DT", "IDL"],
    "LOW": ["RB", "G", "OG", "C", "TE"]
}

# =========================
# LOAD DATA
# =========================

def classify_player_value(w_av):
    if w_av >= 70:
        return "⭐ Estrella"
    elif w_av >= 45:
        return "🔥 Muy bueno"
    elif w_av >= 30:
        return "✔ Titular sólido"
    elif w_av >= 15:
        return "➖ Rotación"
    else:
        return "❌ Bajo impacto"

def load_historical_data():
    df = pd.read_csv(HISTORICAL_CSV)
    df.columns = df.columns.str.lower()

    df = df[[
        "season", "round", "pick", "position",
        "team", "probowls", "allpro", "w_av"
    ]]

    df = df[df["season"] >= 2010].copy()
    df["success"] = df["w_av"] >= 30

    return df


def load_current_board():
    df = pd.read_csv(CURRENT_BOARD_CSV)
    df.columns = df.columns.str.lower()
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
    df = df.dropna(subset=["rank"])
    df["name"] = df["name"].astype(str).str.strip()
    return df


# =========================
# HELPERS
# =========================
def suggest_players_by_position(pick, team="Giants"):
    df = analyze_pick_options(pick)

    target_positions = ["QB", "RB", "WR", "TE", "OT", "OL", "DT", "CB", "EDGE", "LB", "S"]

    selected = []
    used_names = set()

    # 1️⃣ uno por posición (si existe)
    for pos in target_positions:
        candidates = df[
            df["pos"].str.contains(pos, case=False, na=False) &
            ~df["name"].isin(used_names)
        ]

        if not candidates.empty:
            player = candidates.iloc[0]
            selected.append(player)
            used_names.add(player["name"])

    # 2️⃣ completar hasta 15 con BPA
    remaining = df[~df["name"].isin(used_names)]

    combined = pd.concat([pd.DataFrame(selected), remaining], ignore_index=True)

    # 3️⃣ 🔥 ORDENAR TODO POR SCORE
    combined = combined.sort_values(by="score", ascending=False)

    # 4️⃣ coger top 15 final
    return combined.head(15)

def get_pick_label(pick):
    if pick <= 5:
        return "TOP 5"
    elif pick <= 10:
        return "TOP 10"
    elif pick <= 32:
        return "1ª RONDA"
    elif pick <= 64:
        return "2ª RONDA"
    elif pick <= 100:
        return "3a RONDA"
    else:
        return "DÍA 3"
    

def analyze_pick_options(pick, team="Giants", top_n=15):
    df_hist = load_historical_data()
    df_board = load_current_board()

    # 🔥 rango realista alrededor del pick
    options = df_board[
        (df_board["rank"] >= pick - 3) &
        (df_board["rank"] <= pick + 7)
    ].copy()

    options = options.sort_values("rank")

    results = []

    for _, player in options.iterrows():
        pos = player["position"]
        name = player["name"]
        rank = int(player["rank"])

        success, value = compute_historical_metrics(df_hist, pos, pick)
        dist = compute_value_distribution(df_hist, pos, pick)

        if dist is not None:
            star = dist.get("⭐ Estrella", 0)

            good = dist.get("🔥 Muy bueno", 0)
            solid = dist.get("✔ Titular sólido", 0)

            starter = good + solid   # 👈 YA SIN incluir star

            bust = dist.get("❌ Bajo impacto", 0)




        else:
        # fallback realista (day 3 NFL)
            star = 0.02
            starter = 0.20
            bust = 0.60
    

        impact = min(starter + star, 1)
        # 🔥 perfil legible
        profile = f"{int(star*100)}% star | {int(starter*100)}% starter | {int(bust*100)}% bust"

        # 🔥 tipo de jugador
        if bust > 0.5:
            archetype = "High risk"

        elif impact > 0.45:
            archetype = "Good pick"

        elif impact > 0.35:
            archetype = "Starter"

        else:
            archetype = "Rotational"

        results.append({
            "name": name,
            "pos": pos,
            "rank": rank,
            "starter_prob": starter,
            "star_prob": star,
            "bust_prob": bust,
            "impact_prob": impact,
            "value": value if value else 0,
            "profile": profile,
            "type": archetype
        })

    df_results = pd.DataFrame(results)
    if df_results.empty:
        raise ValueError(f"No hay jugadores disponibles para el pick {pick}")

    # 🧠 SCORE BASE (calidad jugador)
    base_score = (
    df_results["star_prob"] * 4 +
    df_results["starter_prob"] * 2 -
    df_results["bust_prob"] * 1.5
)
    

    

    # 🧠 BONUS POSICIONAL (sin destruir lo anterior)
    def positional_bonus(pos):
        level = get_positional_value(pos)
        if level == "HIGH":
            return 0.5
        elif level == "MEDIUM":
            return 0.2
        else:
            return -0.3
    def need_bonus(pos):
        level = get_team_need_level("Giants", pos)
        if level == "HIGH":
            return 0.3
        elif level == "MEDIUM":
            return 0.1
        else:
            return 0
        
    value_bonus = (pick - df_results["rank"]) * 0.02

    df_results["score"] = (
        base_score
        + value_bonus
        + df_results["pos"].apply(positional_bonus)
        + df_results["pos"].apply(need_bonus)
)
    min_score = df_results["score"].min()
    max_score = df_results["score"].max()

    df_results["norm_score"] = (
    (df_results["score"] - min_score) / (max_score - min_score + 1e-6)
)
# 🔥 NUEVO: ranking relativo
    df_results["percentile"] = df_results["score"].rank(method="min", pct=True)

    def classify_pick_hybrid(row):
        score = row["score"]
        norm = row["norm_score"]
        bust = row["bust_prob"]

    # 🔴 filtro absoluto (clave)
        if bust > 0.75:
            return "VERY RISKY"

        if score < -0.8:
            return "WEAK PICK"

    # 🟡 ranking relativo dentro del grupo
        if norm >= 0.85:
            return "BEST AVAILABLE"
        elif norm >= 0.65:
            return "GOOD OPTION"
        elif norm >= 0.4:
            return "OK OPTION"
        else:
            return "LOW VALUE"
    
    '''def classify_pick(score):
        if score >= 0.2:
            return "ELITE PICK"
        elif score >= 0:
            return "GOOD PICK"
        elif score >= -0.25:
            return "OK PICK"
        else:
            return "WEAK PICK"'''

    df_results["type"] = df_results.apply(classify_pick_hybrid, axis=1)
# ordenar después de clasificar
    df_results = df_results.sort_values(by="score", ascending=False)

    return df_results#
    

def classify_pick_norm(s):
    if s >= 0.8:
        return "ELITE PICK"
    elif s >= 0.6:
        return "GOOD PICK"
    elif s >= 0.4:
        return "OK PICK"
    else:
        return "WEAK PICK"

def get_best_alternative_score(df_board, df_hist, pick, current_pos):
    candidates = df_board[df_board["rank"] <= pick + 3].copy()

    scores = []

    for _, row in candidates.iterrows():
        pos = row["position"].upper()

        if pos == current_pos:
            continue

        success, value = compute_historical_metrics(df_hist, pos, pick)

        score = 0

        if pick <= 10:
            good = 0.50
        elif pick <= 32:
            good = 0.35
        else:
            good = 0.25

        if success is not None:
            if success > good:
                score += 2
            elif success > good - 0.1:
                score += 1

        if value is not None:
            if value > 45:
                score += 2
            elif value > 30:
                score += 1

        scores.append(score)

    if not scores:
        return 0

    return max(scores)

def normalize_position(pos):
    return POSITION_MAP.get(pos.upper().strip(), [pos.upper().strip()])


def get_positional_value(pos):
    comps = normalize_position(pos)
    for level in POSITION_VALUE:
        if any(p in comps for p in POSITION_VALUE[level]):
            return level
    return "MEDIUM"


def get_team_need_level(team, pos):
    pos_clean = pos.upper().strip()
    needs = TEAM_NEEDS.get(team, {})

    for level in needs:
        if pos_clean in needs[level]:
            return level

    return "LOW"


def compute_historical_metrics(df, pos, pick):
    comps = normalize_position(pos)

    low, high = get_pick_range(pick)
    df_range = df[(df["pick"] >= low) & (df["pick"] <= high)]

    df_pos = df_range[df_range["position"].isin(comps)]

    if df_pos.empty:
        return None, None

    return df_pos["success"].mean(), df_pos["w_av"].mean()

    # 💥 dividir por rango de pick
def get_pick_range(pick):
    if pick <= 10:
        return (1, 10)
    elif pick <= 32:
        return (11, 32)
    elif pick <= 50:
        return (33, 50)
    elif pick <= 75:
        return (51, 75)
    elif pick <= 100:
        return (76, 100)
    else:
        return (101, 200)




def compute_reach(rank, pick):
    diff = pick - rank

    if diff <= -10:
        return "BIG REACH"
    elif diff <= -5:
        return "REACH"
    elif diff < 0:
        return "SLIGHT REACH"
    elif diff == 0:
        return "VALOR ESPERADO"
    elif diff <= 5:
        return "GOOD VALUE"
    elif diff <= 10:
        return "STEAL"
    else:
        return "BIG STEAL"


def get_board_context(df_board, pick):
    return df_board[df_board["rank"] <= pick + 3]["position"].value_counts()


def get_scarcity_bonus(pos, board_counts):
    count = board_counts.get(pos, 0)
    if count <= 1:
        return 2
    elif count <= 3:
        return 1
    return 0

def compute_value_distribution(df, pos, pick):
    comps = normalize_position(pos)

    low, high = get_pick_range(pick)
    df_range = df[(df["pick"] >= low) & (df["pick"] <= high)]

    df_pos = df_range[df_range["position"].isin(comps)].copy()

    if df_pos.empty:
        return None

    df_pos["tier"] = df_pos["w_av"].apply(classify_player_value)

    return df_pos["tier"].value_counts(normalize=True)

# =========================
# GM LOGIC
# =========================

def get_team_history(df, team, since):
    return df[(df["team"] == team) & (df["season"] >= since)]


def get_position_distribution(df):
    return df["position"].value_counts(normalize=True)


def get_gm_fit(pos, dist):
    return dist.get(pos, 0)


# =========================
# SCORING
# =========================

def grade_pick(success, value, need, reach, pos, scarcity, alt_score):
    score = 0

    # histórico
    if success is not None:
        score += 2 if success > 0.6 else 1 if success > 0.45 else 0

    if value is not None:
        score += 2 if value > 45 else 1 if value > 30 else 0

    # need
    score += 2 if need == "HIGH" else 1 if need == "MEDIUM" else 0

    # positional value
    pv = get_positional_value(pos)
    score += 2 if pv == "HIGH" else 1 if pv == "MEDIUM" else -1

    # scarcity
    score += scarcity

    # reach
    score += 2 if reach == "BIG VALUE" else 1 if reach == "VALUE" else -1 if reach == "REACH" else -2 if reach == "BIG REACH" else 0

    # alternatives
    if score > alt_score:
        score += 1
    elif score < alt_score:
        score -= 1

    # grade
    if score >= 9:
        return "A"
    elif score >= 7:
        return "B"
    elif score >= 5:
        return "C"
    else:
        return "D"


# =========================
# MAIN
# =========================



def analyze_player(name, pick, team="Giants"):
    df_hist = load_historical_data()
    df_board = load_current_board()

    player = df_board[df_board["name"].str.lower().str.contains(name.lower().strip())]
    if player.empty:
        return "Jugador no encontrado"

    player = player.iloc[0]

    pos = player["position"]
    rank = int(player["rank"])

    success, value = compute_historical_metrics(df_hist, pos, pick)
    need = get_team_need_level(team, pos)
    reach = compute_reach(rank, pick)
    dist = compute_value_distribution(df_hist, pos, pick)
    board_counts = get_board_context(df_board, pick)
    scarcity = get_scarcity_bonus(pos, board_counts)
    if scarcity == 2:
        scarcity_txt = "muy pocos disponibles"
    elif scarcity == 1:
        scarcity_txt = "algunos"
    else:
        scarcity_txt = "hay muchos"

    alt_score = get_best_alternative_score(df_board, df_hist, pick, pos)

    # GM data
    schoen = get_team_history(df_hist, "NYG", 2022)
    ravens = get_team_history(df_hist, "BAL", 2015)

    schoen_dist = get_position_distribution(schoen)
    ravens_dist = get_position_distribution(ravens)

    gm_fit = get_gm_fit(pos, schoen_dist)
    ravens_fit = get_gm_fit(pos, ravens_dist)

    grade = grade_pick(success, value, need, reach, pos, scarcity, alt_score)

    success_txt = f"{success:.2f}" if success is not None else "N/A"
    value_txt = f"{value:.1f}" if value is not None else "N/A"
    # =========================
# 📊 DISTRIBUCIÓN + SUMMARY
# =========================

    if dist is not None:
        star = dist.get("⭐ Estrella", 0)
        good = dist.get("🔥 Muy bueno", 0)
        solid = dist.get("✔ Titular sólido", 0)
        bust = dist.get("❌ Bajo impacto", 0)

        starter = good + solid

        summary = (
            f"⭐ {star:.0%} | "
            f"🧱 {starter:.0%} | "
            f"💥 {bust:.0%}"
        )

        dist_txt = "\n".join([f"- {k}: {v:.0%}" for k, v in dist.items()])

    else:
        summary = "N/A"
        dist_txt = "N/A"

    return f"""
{team.upper()} DRAFT ANALYSIS

Player: {player['name']} ({pos})
College: {player.get('college', 'N/A')}

Board rank: #{rank}
Pick: #{pick}
Reach: {reach}

Team need: {need}
Positional value: {get_positional_value(pos)}

📌 Outcome summary:
{summary}
📊 Historical outcomes:
{dist_txt}

📈 Avg value: {value_txt}

📦 Availability: {scarcity_txt}

FINAL GRADE: {grade}
"""


if __name__ == "__main__":

    mode = input("Modo (1 = jugador, 2 = comparar opciones): ")

    if mode == "1":
        pick = int(input("Pick: "))

        df = suggest_players_by_position(pick)

        print("\n🎯 RECOMMENDED PLAYERS:\n")

        df_reset = df.reset_index(drop=True)

        # 🔥 mostrar lista numerada
        for i, row in df_reset.iterrows():
            print(f"{i+1}. {row['name']} ({row['pos']}) - rank #{row['rank']} | score {round(row['score'], 2)}")

        # 🔥 selección por número
        print("\n👉 Selecciona jugador (número):\n")
        choice = int(input("Opción: "))

        # 🔥 control básico de errores
        if choice < 1 or choice > len(df_reset):
            print("❌ Opción inválida")
        else:
            name = df_reset.iloc[choice - 1]["name"]
            print(analyze_player(name, pick))

    elif mode == "2":
        pick = int(input("Pick: "))
        df = analyze_pick_options(pick)

        print("\n📊 BEST OPTIONS AVAILABLE:\n")

        df_display = df.copy()

        # 🔥 convertir a %
        df_display["starter_prob"] = (df_display["starter_prob"] * 100).round(2).astype(str) + "%"
        df_display["star_prob"] = (df_display["star_prob"] * 100).round(2).astype(str) + "%"
        df_display["bust_prob"] = (df_display["bust_prob"] * 100).round(2).astype(str) + "%"

        # 🔥 redondear scores
        df_display["score"] = df_display["score"].round(2)
        df_display["norm_score"] = df_display["norm_score"].round(2)

        # 🔥 nombres más claros
        df_display = df_display.rename(columns={
            "starter_prob": "Starter %",
            "star_prob": "Star %",
            "bust_prob": "Bust %"
        })

        # 🔥 columnas finales (orden lógico)
        cols = [
            "name", "pos", "rank",
            "profile",
            "Starter %", "Star %", "Bust %",
            "type", "score"
        ]

        # =========================
        # 📌 INSIGHT PRINCIPAL
        # =========================

        best = df.iloc[0]

        # 👉 NUEVO: etiqueta del pick + rango
        pick_label = get_pick_label(pick)
        low, high = get_pick_range(pick)

        print(f"📍 PICK #{pick} — {pick_label} (rango {low}-{high})\n")

        print("📌 DRAFT INSIGHT:\n")

        # 👉 NUEVO: probabilidades claras arriba
        star = int(best["star_prob"] * 100)
        starter = int(best["starter_prob"] * 100)
        bust = int(best["bust_prob"] * 100)

        print(f"→ Mejor opción: {best['name']} ({best['pos']})")
        print(f"→ Probabilidades: ⭐ {star}% | 🧱 {starter}% | 💥 {bust}%")
        print(f"→ Perfil: {best['profile']}")

        # 🔥 contexto del pick
        if best["score"] < -0.5:
            print("⚠️ Clase muy débil (alto riesgo de bust)")
            print("→ Recomendación: trade down urgente\n")

        elif best["score"] < -0.2:
            print("⚠️ Clase floja")
            print("→ Recomendación: considerar trade down\n")

        else:
            print("✅ Buen valor para el pick")
            print("→ Recomendación: pick sólido\n")

    # =========================
    # 📊 TABLA FINAL
    # =========================
        cols = [
            "name", "pos", "rank",
            "profile",
            "Starter %", "Star %", "Bust %",
            "type", "score"
        ]
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 1000)
        print(df_display[cols])
        print("\n📎 NOTA SOBRE EL SCORE:")
        print(
            "El score combina: Upside, porcentaje titular, porcentaje bust, reach/value, valor posicional, necesidad equipo \n"
        )
        print("• Score > 2 → Pick élite\n"
            "• Score 1 - 2 → Buen pick\n"
            "• Score 0 - 1 → Aceptable\n"
            "• Score < 0 → Riesgo alto / poco valor\n"
)
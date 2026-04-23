import pandas as pd

# =========================
# CONFIG
# =========================

HISTORICAL_CSV = "data/prospects.csv"
CURRENT_BOARD_CSV = "data/prospects_current.csv"

TEAM_NEEDS = {
    "Giants": {
        "HIGH": ["IOL", "OL", "DT", "DL", "CB"],
        "MEDIUM": ["LB", "WR", "S"],
        "LOW": ["OT", "EDGE", "RB", "TE", "QB"]
    },
    "Patriots": {
        "HIGH": ["WR", "OL", "EDGE"],
        "MEDIUM": ["S", "CB"]
    },

    "Cardinals": {
        "HIGH": ["WR", "EDGE", "CB"],
        "MEDIUM": ["DL", "OL"]
    },

    "Commanders": {
        "HIGH": ["OT", "EDGE", "CB"],
        "MEDIUM": ["WR", "LB"]
    },

    "Chargers": {
        "HIGH": ["WR", "CB", "DL"],
        "MEDIUM": ["EDGE", "OL"]
    },

    "Titans": {
        "HIGH": ["OL", "WR", "CB"],
        "MEDIUM": ["DL", "EDGE"]
    },

    "Falcons": {
        "HIGH": ["EDGE", "CB", "DL"],
        "MEDIUM": ["WR", "OL"]
    },

    "Bears": {
        "HIGH": ["WR", "EDGE", "OL"],
        "MEDIUM": ["CB", "S"]
    },

    "Jets": {
        "HIGH": ["OL", "WR", "DL"],
        "MEDIUM": ["S", "EDGE"]
    },

    "Saints": {
        "HIGH": ["OL", "QB", "WR"],
        "MEDIUM": ["DL", "EDGE"]
    },

    "Colts": {
        "HIGH": ["CB", "WR", "OL"],
        "MEDIUM": ["DL", "LB"]
    },

    "Seahawks": {
        "HIGH": ["OL", "DL", "LB"],
        "MEDIUM": ["WR", "CB"]
    },

    "Jaguars": {
        "HIGH": ["CB", "DL", "WR"],
        "MEDIUM": ["OL", "EDGE"]
    },

    "Bengals": {
        "HIGH": ["OL", "DL", "CB"],
        "MEDIUM": ["WR", "EDGE"]
    },

    "Rams": {
        "HIGH": ["EDGE", "OL", "CB"],
        "MEDIUM": ["WR", "DL"]
    },

    "Steelers": {
        "HIGH": ["OT", "CB", "WR"],
        "MEDIUM": ["DL", "EDGE"]
    },

    "Dolphins": {
        "HIGH": ["OL", "DL", "CB"],
        "MEDIUM": ["LB", "S"]
    },

    "Eagles": {
        "HIGH": ["CB", "DL", "OL"],
        "MEDIUM": ["WR", "EDGE"]
    },

    "Texans": {
        "HIGH": ["DL", "CB", "OL"],
        "MEDIUM": ["WR", "EDGE"]
    },

    "Packers": {
        "HIGH": ["OL", "S", "DL"],
        "MEDIUM": ["WR", "CB"]
    },

    "Buccaneers": {
        "HIGH": ["OL", "EDGE", "CB"],
        "MEDIUM": ["WR", "DL"]
    },

    "Cowboys": {
        "HIGH": ["OL", "LB", "DL"],
        "MEDIUM": ["WR", "CB"]
    },

    "Broncos": {
        "HIGH": ["WR", "QB", "OL"],
        "MEDIUM": ["DL", "EDGE"]
    },

    "Raiders": {
        "HIGH": ["QB", "WR", "OL"],
        "MEDIUM": ["DL", "CB"]
    },

    "Vikings": {
        "HIGH": ["QB", "DL", "CB"],
        "MEDIUM": ["WR", "OL"]
    },

    "Lions": {
        "HIGH": ["CB", "EDGE", "OL"],
        "MEDIUM": ["WR", "DL"]
    },

    "Bills": {
        "HIGH": ["WR", "CB", "DL"],
        "MEDIUM": ["OL", "S"]
    },

    "Chiefs": {
        "HIGH": ["WR", "OT", "DL"],
        "MEDIUM": ["CB", "EDGE"]
    },

    "49ers": {
        "HIGH": ["OL", "CB", "DL"],
        "MEDIUM": ["WR", "EDGE"]
    },

    "Ravens": {
        "HIGH": ["OL", "WR", "CB"],
        "MEDIUM": ["DL", "EDGE"]
    },

    "Browns": {
        "HIGH": ["QB", "WR", "OL"],
        "MEDIUM": ["DL", "EDGE"]
    },

    "Panthers": {
        "HIGH": ["WR", "OL", "CB"],
        "MEDIUM": ["DL", "EDGE"]
    }

}

POSITION_MAP = {
    "EDGE": ["DE", "EDGE"],
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

    # 🔥 mantener nombres si existen
    cols = [
        "season", "round", "pick", "position",
        "team", "probowls", "allpro", "w_av"
    ]

    if "pfr_player_name" in df.columns:
        cols.append("pfr_player_name")

    df = df[cols]

    # 🔥 renombrar directamente aquí (MUY IMPORTANTE)
    if "pfr_player_name" in df.columns:
        df = df.rename(columns={"pfr_player_name": "name"})

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
def select_team():
    teams = list(TEAM_NEEDS.keys())

    print("\n🏈 Equipos disponibles:\n")
    for i, t in enumerate(teams):
        print(f"{i+1}. {t}")

    while True:
        try:
            choice = int(input("\nSelecciona equipo (número): "))

            if 1 <= choice <= len(teams):
                return teams[choice - 1]
            else:
                print("❌ Número fuera de rango")

        except ValueError:
            print("❌ Introduce un número válido")

def get_position_by_pick_range(df):
    df = df.copy()
    
    def pick_bucket(p):
        if p <= 10:
            return "TOP10"
        elif p <= 32:
            return "R1"
        elif p <= 64:
            return "R2"
        else:
            return "LATE"

    df["bucket"] = df["pick"].apply(pick_bucket)

    # distribución normalizada por bucket + posición
    return df.groupby(["bucket", "position"]).size().unstack(fill_value=0).apply(lambda x: x / x.sum(), axis=1)

def classify_gm_style_by_pick(pos, pick, schoen_hist, ravens_hist):

    # =========================
    # BUCKET
    # =========================
    if pick <= 10:
        bucket = "TOP10"
    elif pick <= 32:
        bucket = "R1"
    elif pick <= 64:
        bucket = "R2"
    else:
        bucket = "LATE"

    comps = normalize_position(pos)

    # =========================
    # DISTRIBUCIONES
    # =========================
    schoen_pick_dist = get_position_by_pick_range(schoen_hist)
    ravens_pick_dist = get_position_by_pick_range(ravens_hist)

    schoen_global = get_position_distribution(schoen_hist)
    ravens_global = get_position_distribution(ravens_hist)

    # =========================
    # SCORES PICK
    # =========================
    if bucket in schoen_pick_dist.index:
        schoen_pick_score = sum(schoen_pick_dist.loc[bucket].get(p, 0) for p in comps)
    else:
        schoen_pick_score = 0

    if bucket in ravens_pick_dist.index:
        ravens_pick_score = sum(ravens_pick_dist.loc[bucket].get(p, 0) for p in comps)
    else:
        ravens_pick_score = 0

    # =========================
    # SCORES GLOBAL
    # =========================
    schoen_global_score = sum(schoen_global.get(p, 0) for p in comps)
    ravens_global_score = sum(ravens_global.get(p, 0) for p in comps)

    # =========================
    # SAMPLE SIZE (CLAVE)
    # =========================
    def pick_bucket(p):
        if p <= 10:
            return "TOP10"
        elif p <= 32:
            return "R1"
        elif p <= 64:
            return "R2"
        else:
            return "LATE"

    schoen_samples = schoen_hist[schoen_hist["pick"].apply(lambda p: pick_bucket(p) == bucket)].shape[0]
    ravens_samples = ravens_hist[ravens_hist["pick"].apply(lambda p: pick_bucket(p) == bucket)].shape[0]

    # =========================
    # PESO DINÁMICO (🔥 clave)
    # =========================
    total_samples = min(schoen_samples, ravens_samples)

    alpha = min(1, total_samples / 10)  
    # → si hay pocos datos → alpha bajo → más peso global

    # =========================
    # SCORE FINAL (mezcla)
    # =========================
    schoen_score = alpha * schoen_pick_score + (1 - alpha) * schoen_global_score
    ravens_score = alpha * ravens_pick_score + (1 - alpha) * ravens_global_score

    diff = schoen_score - ravens_score

    # =========================
    # CLASIFICACIÓN
    # =========================
    if schoen_score < 0.05 and ravens_score < 0.05:
        return "🎲 Unusual pick"
    elif diff > 0.03:
        return "🟦 Schoen style"
    elif diff < -0.03:
        return "🟥 Harbaugh style"
    else:
        return "⚖️ Neutral"
    
def classify_gm_style(pos, schoen_dist, ravens_dist):
    schoen_score = schoen_dist.get(pos, 0)
    ravens_score = ravens_dist.get(pos, 0)

    if schoen_score > ravens_score * 1.2:
        return "🟦 Schoen style"
    elif ravens_score > schoen_score * 1.2:
        return "🟥 Harbaugh style"
    else:
        return "⚖️ Neutral"

def suggest_players_by_position(pick, team):
    df = analyze_pick_options(pick, team)

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
    

def analyze_pick_options(pick, team, top_n=15):
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
        level = get_team_need_level(team, pos)
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
    comps = normalize_position(pos)
    needs = TEAM_NEEDS.get(team, {})

    for level in needs:
        for need in needs[level]:
            mapped = normalize_position(need)
            if any(p in comps for p in mapped):
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
    ravens = get_team_history(df_hist, "BAL", 2008)

    schoen_dist = get_position_distribution(schoen)
    ravens_dist = get_position_distribution(ravens)

    gm_fit = get_gm_fit(pos, schoen_dist)
    ravens_fit = get_gm_fit(pos, ravens_dist)
    gm_style = classify_gm_style_by_pick(pos, pick, schoen, ravens)
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

        order = [
            "⭐ Estrella",
            "🔥 Muy bueno",
            "✔ Titular sólido",
            "➖ Rotación",
            "❌ Bajo impacto"
        ]

        dist_txt = "\n".join([
            f"- {k}: {dist.get(k, 0):.0%}"
            for k in order if k in dist
        ])
        
        #dist_txt = "\n".join([f"- {k}: {v:.0%}" for k, v in dist.items()])

    else:
        summary = "N/A"
        dist_txt = "N/A"

    return f"""
{team.upper()} DRAFT ANALYSIS

Player: {player['name']} ({pos})
College: {player['college']}
{f"GM Style: {gm_style}" if team == "Giants" else ""}

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
        team = select_team()
        print(f"\n📊 Analizando para: {team}\n")        
        pick = int(input("Pick: "))
        
        # 🔥 cargar datos primero
        df = suggest_players_by_position(pick, team)
        df = df.reset_index(drop=True)

        import matplotlib.pyplot as plt

        # =====================================================
        # =====================================================
        # 📊 GRÁFICO 1: TOP OPTIONS (SOLUCIÓN NameError)
        # =====================================================
        import matplotlib.pyplot as plt
        import numpy as np  # <--- IMPORTANTE: Esto soluciona tu error

        # Seleccionamos los 10 mejores y ordenamos para que el mejor esté arriba
        df_top = df.head(10).sort_values(by="score", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 6))

        # Gradiente de color: Rojo (bajo) a Verde (alto)
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(df_top))) 

        bars = ax.barh(df_top["name"], df_top["score"], color=colors, edgecolor='black', alpha=0.8)

        # Añadir etiquetas de valor al final de la barra
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, 
                    f'{width:.2f}', va='center', fontsize=10, fontweight='bold')

        ax.set_title(f"Top Board Options — Pick {pick} ({team})", fontsize=14, pad=15, fontweight='bold')
        ax.set_xlabel("Prospect Score", fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.3)

        plt.tight_layout()
        plt.show()

        # =========================
        # =====================================================
        # 📊 GRÁFICO 2: POSITIONS AVAILABLE (SOLUCIÓN FINAL)
        # =====================================================
        import matplotlib.pyplot as plt
        import numpy as np

        # 1. Usamos el nombre exacto que aparece en tu lista: 'pos'
        if 'pos' in df.columns:
            # Conteo de posiciones en el Top 15 disponible
            pos_counts = df.head(15)['pos'].value_counts()

            fig, ax = plt.subplots(figsize=(10, 6))

            # Paleta de colores profesional (Paired da colores distintos a cada posición)
            colors = plt.cm.Paired(np.linspace(0, 1, len(pos_counts)))

            bars = ax.bar(pos_counts.index, pos_counts.values, 
                        color=colors, edgecolor='black', alpha=0.8)

            # Añadir el número de jugadores encima de cada barra
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                        f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')

            # Estética y Títulos
            ax.set_title(f"Draft Depth by Position (Top 15) — Pick {pick}", fontsize=14, pad=20, fontweight='bold')
            ax.set_ylabel("Number of Players", fontsize=11)
            ax.set_xlabel("Position Group", fontsize=11)

            # Solo números enteros en el eje Y para evitar decimales como 1.5
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            
            # Limpieza de bordes
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            plt.tight_layout()
            plt.show()
        else:
            print("Error: La columna 'pos' no se encuentra en el DataFrame.")
        '''
        # =========================
        # =========================
        # 📊 GRÁFICO 3: RISK VS UPSIDE (VERSIÓN PRO)
        # =========================
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(figsize=(12, 8))

        # =========================
        # 🔥 JITTER (CLAVE)
        # =========================
        np.random.seed(42)

        df["x_plot"] = df["bust_prob"] + np.random.uniform(-0.007, 0.007, len(df))
        df["y_plot"] = df["star_prob"] + np.random.uniform(-0.004, 0.004, len(df))

        # =========================
        # 🔥 TAMAÑO
        # =========================
        sizes = df["impact_prob"] * 300 + 80

        # =========================
        # 🔥 ESCALA DINÁMICA REAL
        # =========================
        # =========================
        # 🔥 ESCALA CONTROLADA (FIX REAL)
        # =========================
        margin_x = 0.03
        margin_y = 0.03

        x_min = max(0, df["bust_prob"].min() - margin_x)
        x_max = df["bust_prob"].max() + margin_x

        y_min = max(0, df["star_prob"].min() - margin_y)
        y_max = df["star_prob"].max() + margin_y

        # 🔥 asegurar rango mínimo (CLAVE)
        if (x_max - x_min) < 0.15:
            center = (x_max + x_min) / 2
            x_min = max(0, center - 0.075)
            x_max = center + 0.075

        if (y_max - y_min) < 0.10:
            center = (y_max + y_min) / 2
            y_min = max(0, center - 0.05)
            y_max = center + 0.05

        # 🔥 limitar outliers (también importante)
        x_max = min(x_max, 0.6)
        y_max = min(y_max, 0.3)

        # 🔥 SOLO AQUÍ se fijan los límites
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # =========================
        # 🔥 CUADRANTES (FIJOS NFL)
        # =========================
        x_mid = 0.25
        y_mid = 0.15

        ax.axvspan(x_min, x_mid, ymin=(y_mid - y_min)/(y_max - y_min), ymax=1,
                alpha=0.05, color="green")

        ax.axvspan(x_mid, x_max, ymin=(y_mid - y_min)/(y_max - y_min), ymax=1,
                alpha=0.05, color="orange")

        ax.axvspan(x_min, x_mid, ymin=0, ymax=(y_mid - y_min)/(y_max - y_min),
                alpha=0.05, color="blue")

        ax.axvspan(x_mid, x_max, ymin=0, ymax=(y_mid - y_min)/(y_max - y_min),
                alpha=0.05, color="red")

        # =========================
        # 🔥 SCATTER
        # =========================
        scatter = ax.scatter(
            df["x_plot"],
            df["y_plot"],
            c=df["score"],
            cmap="coolwarm",
            s=sizes,
            edgecolors="black",
            zorder=3
        )

        # =========================
        # 🔥 BEST PLAYER
        # =========================
        best = df.iloc[0]

        ax.scatter(
            best["x_plot"],
            best["y_plot"],
            s=450,
            facecolors="none",
            edgecolors="black",
            linewidths=2,
            zorder=4
        )

        # =========================
        # 🔥 LABELS LIMPIOS
        # =========================
        top5_names = set(df.head(5)["name"])

        for i, row in df.iterrows():

            x = row["x_plot"]
            y = row["y_plot"]

            name_parts = row["name"].split()
            label = f"{name_parts[0][0]}. {name_parts[-1]}"

            if row["name"] in top5_names:
                # 🔥 offset dinámico (MUY IMPORTANTE)
                offset_x = (x_max - x_min) * (0.03 if row["bust_prob"] < x_mid else -0.03)
                offset_y = (y_max - y_min) * (0.03 if row["star_prob"] < y_mid else -0.03)

                label_x = np.clip(x + offset_x, x_min + 0.01, x_max - 0.01)
                label_y = np.clip(y + offset_y, y_min + 0.01, y_max - 0.01)

                ax.text(
                    label_x,
                    label_y,
                    label,
                    fontsize=10,
                    weight="bold"
                )

                ax.plot(
                    [x, label_x],
                    [y, label_y],
                    color="gray",
                    linewidth=0.7,
                    alpha=0.7
                )

            elif i < 10:   # solo top 10
                ax.text(x, y, label, fontsize=7, alpha=0.6)

        # =========================
        # 🔥 LÍNEAS DE CORTE
        # =========================
        ax.axvline(x=x_mid, linestyle="--", alpha=0.5)
        ax.axhline(y=y_mid, linestyle="--", alpha=0.5)
        # 🔥 evitar que un bust loco rompa el gráfico
        x_max = min(x_max, 0.6)
        y_max = min(y_max, 0.3)

        # =========================
        # 🔥 ETIQUETAS CUADRANTES (FUERA)
        # =========================
        ax.text(0.02, 0.98, "Elite Upside",
                transform=ax.transAxes, fontsize=10, va="top")

        ax.text(0.98, 0.98, "Risky",
                transform=ax.transAxes, fontsize=10, va="top", ha="right")

        ax.text(0.02, 0.02, "Safe",
                transform=ax.transAxes, fontsize=10, va="bottom")

        ax.text(0.98, 0.02, "Low Value",
                transform=ax.transAxes, fontsize=10, va="bottom", ha="right")

        # =========================
        # 🔥 EJES
        # =========================
        ax.set_xticks(np.arange(round(x_min, 2), round(x_max + 0.001, 2), 0.05))
        ax.set_yticks(np.arange(round(y_min, 2), round(y_max + 0.001, 2), 0.02))

        ax.set_xlabel("Bust Probability")
        ax.set_ylabel("Star Probability")

        ax.set_title(f"Risk vs Upside — Pick {pick} ({team})", fontsize=13)

        # =========================
        # 🔥 COLORBAR
        # =========================
        fig.colorbar(scatter, ax=ax, label="Score")

        # =========================
        # 🔥 ESTÉTICA FINAL
        # =========================
        ax.grid(alpha=0.35, linestyle="--")

        plt.tight_layout()
        plt.show()'''

        # =========================
        # =========================
        # =========================
        # 📊 GRÁFICO 3: VERSIÓN ULTRA-DINÁMICA Y BLINDADA
        # =========================
        import matplotlib.pyplot as plt
        import numpy as np

        # 1. GENERACIÓN DE COORDENADAS CON JITTER
        np.random.seed(42)
        df["x_plot"] = df["bust_prob"] + np.random.uniform(-0.003, 0.003, len(df))
        df["y_plot"] = df["star_prob"] + np.random.uniform(-0.002, 0.002, len(df))

        fig, ax = plt.subplots(figsize=(12, 8))

        # =====================================================
        # 2. CÁLCULO DE LÍMITES DINÁMICOS (Súper Adaptables)
        # =====================================================
        # Calculamos el rango real de los datos
        raw_x_min, raw_x_max = df["bust_prob"].min(), df["bust_prob"].max()
        raw_y_max = df["star_prob"].max()

        # Margen dinámico: Si los datos están muy agrupados, damos un margen fijo mínimo
        # para que las etiquetas respiren (0.05 en X, 0.02 en Y mínimo)
        x_padding = max(df["bust_prob"].std() * 0.5, 0.05)
        y_padding = max(df["star_prob"].std() * 0.5, 0.01)

        x_min = max(0, raw_x_min - x_padding)
        x_max = raw_x_max + x_padding
        y_min = 0 # Siempre empezamos en 0 para ver la base
        y_max = raw_y_max + y_padding 

        # --- ELIMINADO: y_max = max(y_max, 0.10) ---
        # Ahora el gráfico se ajustará si el máximo es 0.02 o si es 0.30

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # 3. PUNTOS DE CORTE DINÁMICOS
        x_mid = df["bust_prob"].median()
        y_mid = df["star_prob"].median()

        # 4. 🧠 FONDOS DE CUADRANTE BLINDADOS (Solución para el error en 105)
        # Usamos fill_between en lugar de axvspan para mayor control en límites dinámicos
        ax.fill_between([x_min, x_mid], y_mid, y_max, color='#eaffea', zorder=0)  # Alto Potencial (Verde)
        ax.fill_between([x_mid, x_max], y_mid, y_max, color='#fffdea', zorder=0)  # Riesgo / Boom (Amarillo)
        ax.fill_between([x_min, x_mid], y_min, y_mid, color='#f0f4ff', zorder=0)  # Seguro / Titular (Azul)
        ax.fill_between([x_mid, x_max], y_min, y_mid, color='#ffebeb', zorder=0)  # Bajo Valor (Rojo)

        # Líneas divisoras claras y finas
        ax.axvline(x=x_mid, color='black', linestyle='--', alpha=0.15, lw=1.0)
        ax.axhline(y=y_mid, color='black', linestyle='--', alpha=0.15, lw=1.0)

        # 5. SCATTER PLOT
        scatter = ax.scatter(
            df["x_plot"], df["y_plot"],
            c=df["score"], cmap="RdYlGn",
            s=df["impact_prob"] * 500 + 150, 
            edgecolors="black", linewidths=1, zorder=4
        )

        # 6. ETIQUETADO RADIAL AUTOMÁTICO
        top_players = df.head(15).reset_index()
        for i, row in top_players.iterrows():
            # Ángulo diferente para evitar amontonamiento
            angle = (i * (360 / len(top_players))) * (np.pi / 180) 
            dist = 45 
            
            x_off, y_off = dist * np.cos(angle), dist * np.sin(angle)
            
            # Empuje extra si están en los bordes
            if row["x_plot"] > x_max - (x_max-x_min)*0.10: x_off = -abs(x_off) - 10
            if row["x_plot"] < x_min + (x_max-x_min)*0.10: x_off = abs(x_off) + 10

            ax.annotate(
                row["name"],
                xy=(row["x_plot"], row["y_plot"]),
                xytext=(x_off, y_off),
                textcoords='offset points',
                fontsize=8, weight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8, ec='none'),
                arrowprops=dict(
                    arrowstyle='->',
                    connectionstyle="arc3,rad=0.1",
                    color='black', alpha=0.3, lw=0.7
                ),
                zorder=5
            )

        # 7. TÍTULOS Y ESTÉTICA (Solucionado para 105)
        ax.set_title(f"Riesgo vs. Potencial — Pick {pick} ({team})", fontsize=15, pad=20, weight='bold')
        plt.colorbar(scatter, label="Score de Calidad")

        # Etiquetas fijas en las esquinas basadas en los límites actuales
        style = {'fontsize': 11, 'fontweight': 'black', 'alpha': 0.3}
        ax.text(x_min+(x_max-x_min)*0.03, y_max-(y_max-y_min)*0.03, "ALTO POTENCIAL / ELITE", color='green', va='top', **style)
        ax.text(x_max-(x_max-x_min)*0.03, y_max-(y_max-y_min)*0.03, "RIESGO / BOOM", color='orange', va='top', ha='right', **style)
        ax.text(x_min+(x_max-x_min)*0.03, y_min+(y_max-y_min)*0.03, "SEGURO / TITULAR", color='blue', va='bottom', **style)
        ax.text(x_max-(x_max-x_min)*0.03, y_min+(y_max-y_min)*0.03, "BAJO VALOR / ROTACION", color='red', va='bottom', ha='right', **style)

        plt.tight_layout()
        plt.show()

        # =========================
        # 🧠 GM STYLE DATA
        # =========================
        df_hist = load_historical_data()
        schoen = get_team_history(df_hist, "NYG", 2022)
        ravens = get_team_history(df_hist, "BAL", 2008)

        print("\n🎯 RECOMMENDED PLAYERS:\n")

        # =========================
        # 📋 LISTA JUGADORES
        # =========================
        for i, row in df.iterrows():
            pos = row["pos"]

            if team == "Giants":
                gm_style = classify_gm_style_by_pick(pos, pick, schoen, ravens)
            else:
                gm_style = ""

            print(
                f"{i+1}. {row['name']} ({row['pos']}) "
                f"- rank #{row['rank']} | score {round(row['score'], 2)} {gm_style}"
            )

        # =========================
        # 🎯 SELECCIÓN
        # =========================
        #print("\n👉 Selecciona jugador (número):\n")
        choice = int(input("\n👉 Selecciona jugador (número):"))

        if choice < 1 or choice > len(df):
            print("❌ Opción inválida")
        else:
            name = df.iloc[choice - 1]["name"]
            print(analyze_player(name, pick, team))

    elif mode == "2":
        team = select_team()
        print(f"\n📊 Analizando para: {team}\n")
        pick = int(input("Pick: "))
        df = analyze_pick_options(pick, team)

        print("\n📊 BEST OPTIONS AVAILABLE:\n")

        df_display = df.copy()

        df_display["starter_prob"] = (df_display["starter_prob"] * 100).round(2).astype(str) + "%"
        df_display["star_prob"] = (df_display["star_prob"] * 100).round(2).astype(str) + "%"
        df_display["bust_prob"] = (df_display["bust_prob"] * 100).round(2).astype(str) + "%"

        df_display["score"] = df_display["score"].round(2)
        df_display["norm_score"] = df_display["norm_score"].round(2)

        df_display = df_display.rename(columns={
            "starter_prob": "Starter %",
            "star_prob": "Star %",
            "bust_prob": "Bust %"
        })

        best = df.iloc[0]

        pick_label = get_pick_label(pick)
        low, high = get_pick_range(pick)

        print(f"📍 PICK #{pick} — {pick_label} (rango {low}-{high})\n")

        print("📌 DRAFT INSIGHT:\n")

        star = int(best["star_prob"] * 100)
        starter = int(best["starter_prob"] * 100)
        bust = int(best["bust_prob"] * 100)

        print(f"→ Mejor opción: {best['name']} ({best['pos']})")
        print(f"→ Probabilidades: ⭐ {star}% | 🧱 {starter}% | 💥 {bust}%")
        print(f"→ Perfil: {best['profile']}")

        if best["score"] < -0.5:
            print("⚠️ Clase muy débil → trade down urgente\n")
        elif best["score"] < -0.2:
            print("⚠️ Clase floja → considerar trade down\n")
        else:
            print("✅ Buen valor → pick sólido\n")

        cols = [
            "name", "pos", "rank",
            "profile",
            "Starter %", "Star %", "Bust %",
            "type", "score"
        ]

        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 1000)
        print(df_display[cols])
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from analyze_player import (
    suggest_players_by_position,
    analyze_player,
    load_historical_data,
    get_team_history,
    classify_gm_style_by_pick,
    compute_reach
)

# =========================
# CONFIG & AUTH
# =========================
st.set_page_config(layout="wide", page_title="NFL Draft Analyzer")

password = st.sidebar.text_input("Password", type="password")
if password != "draft123":
    st.info("Please enter password in the sidebar.")
    st.stop()

# =========================
# DATA LOAD
# =========================
st.title("🏈 NFL Draft Analyzer")
pick = st.slider("Select Pick", 1, 256, 5)

# Obtenemos los datos
df = suggest_players_by_position(pick).reset_index(drop=True)

# IMPORTANTE: Crear las columnas de Jitter para que no de KeyError
np.random.seed(42)
df["x_plot"] = df["bust_prob"] + np.random.uniform(-0.005, 0.005, len(df))
df["y_plot"] = df["star_prob"] + np.random.uniform(-0.003, 0.003, len(df))

best = df.iloc[0]

# =========================
# 🧠 RECOMENDACIÓN TOP
# =========================
st.success(f"### 🧠 Best Option: {best['name']} ({best['pos']})")

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("⭐ Star", f"{int(best['star_prob']*100)}%")
col_m2.metric("🧱 Starter", f"{int(best['starter_prob']*100)}%")
col_m3.metric("💥 Bust", f"{int(best['bust_prob']*100)}%")

# =========================
# 📊 GRÁFICOS
# =========================
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Positions Available (Top 15)")
    # Usamos 'pos' que es como se llama en tu dataframe
    counts = df.head(15)["pos"].value_counts()
    fig1, ax1 = plt.subplots()
    
    # Colores por importancia de posición
    colors = plt.cm.Paired(np.linspace(0, 1, len(counts)))
    bars = ax1.bar(counts.index, counts.values, color=colors, edgecolor="black")
    
    ax1.set_ylabel("Players")
    ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    st.pyplot(fig1)

with col2:
    st.subheader("Risk vs Upside")
    fig2, ax2 = plt.subplots(figsize=(10, 7))

    # 1. Límites dinámicos (LA MEJORA CLAVE)
    y_max_data = df["star_prob"].max()
    x_max_data = df["bust_prob"].max()
    
    y_limit = max(0.05, y_max_data + 0.02)
    x_limit_max = max(0.40, x_max_data + 0.05)
    x_limit_min = max(0, df["bust_prob"].min() - 0.05)

    ax2.set_ylim(-0.005, y_limit)
    ax2.set_xlim(x_limit_min, x_limit_max)

    # 2. Cuadrantes (Fondo de color)
    x_mid = df["bust_prob"].median()
    y_mid = df["star_prob"].median()
    
    ax2.fill_between([x_limit_min, x_mid], y_mid, y_limit, color='#eaffea', alpha=0.3) # Elite
    ax2.fill_between([x_mid, x_limit_max], y_mid, y_limit, color='#fffdea', alpha=0.3) # Risk
    ax2.fill_between([x_limit_min, x_mid], -0.01, y_mid, color='#f0f4ff', alpha=0.3) # Safe
    ax2.fill_between([x_mid, x_limit_max], -0.01, y_mid, color='#ffebeb', alpha=0.3) # Low

    # 3. Scatter
    scatter = ax2.scatter(
        df["x_plot"], df["y_plot"],
        c=df["score"], cmap="RdYlGn",
        s=df["impact_prob"] * 500 + 100,
        edgecolors="black", zorder=3
    )

    # 4. Etiquetas de los mejores
    for i, row in df.head(8).iterrows():
        ax2.annotate(
            row["name"],
            xy=(row["x_plot"], row["y_plot"]),
            xytext=(5, 5), textcoords='offset points',
            fontsize=9, weight='bold', zorder=5
        )

    ax2.set_xlabel("Bust Risk →")
    ax2.set_ylabel("Star Potential ↑")
    st.pyplot(fig2)

# ... El resto de tu código de tabla y análisis individual ...

# =========================
# 📋 TABLE
# =========================
st.subheader("🎯 Recommended Players para el Pick Elegido")
st.dataframe(df[["name", "pos", "rank", "score"]])

# =========================
# 👤 SELECT PLAYER
# =========================
st.markdown("## 👤 Select Player")

options = [
    f"{row['name']} ({row['pos']}) - score {round(row['score'],2)}"
    for _, row in df.iterrows()
]

selected = st.selectbox("", options, label_visibility="collapsed")

# =========================
# 🧠 ANALYSIS
# =========================
if selected:
    idx = options.index(selected)
    player = df.iloc[idx]

    st.markdown("---")

    st.markdown(f"## 🏈 {player['name']} ({player['pos']})")

    col1, col2, col3 = st.columns(3)
    col1.metric("⭐ Star", f"{int(player['star_prob']*100)}%")
    col2.metric("🧱 Starter", f"{int(player['starter_prob']*100)}%")
    col3.metric("💥 Bust", f"{int(player['bust_prob']*100)}%")

    st.markdown("### 🧠 Draft Insight")

    colA, colB, colC = st.columns(3)
    colA.metric("📍 Rank", f"#{player['rank']}")
    colB.metric("📊 Score", round(player["score"],2))
    colC.metric("🎯 Type", player["type"])

    # GM STYLE + REACH
    df_hist = load_historical_data()
    schoen = get_team_history(df_hist, "NYG", 2022)
    ravens = get_team_history(df_hist, "BAL", 2008)

    gm_style = classify_gm_style_by_pick(player["pos"], pick, schoen, ravens)
    reach = compute_reach(player["rank"], pick)

    colD, colE = st.columns(2)
    colD.metric("🧠 GM Style", gm_style)
    colE.metric("📏 Reach", reach)

    st.markdown("### 📊 Player Profile")

    st.progress(player["star_prob"])
    st.caption("Star potential")

    st.progress(player["starter_prob"])
    st.caption("Starter probability")

    st.progress(player["bust_prob"])
    st.caption("Bust risk")

    with st.expander("📄 Full analysis"):
        st.text(analyze_player(player["name"], pick))
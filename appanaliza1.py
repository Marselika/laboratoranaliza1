import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configurare pagină
st.set_page_config(
    page_title="Dashboard Energie România",
    page_icon="⚡",
    layout="wide"
)

# CSS personalizat pentru design plăcut
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTitle {
        color: #1e3a8a;
        font-size: 3rem !important;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# Încărcare date
@st.cache_data
def load_data():
    df = pd.read_csv("energie_transformata.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()

# Titlu principal
st.title("⚡ Dashboard Analiza Energiei Electrice România")
st.markdown("---")

# Sidebar pentru filtre
st.sidebar.header("🎛️ Configurare Analiză")

# Selector tip analiză
tip_analiza = st.sidebar.selectbox(
    "Selectează tipul de analiză:",
    ["📊 Surse de Energie", "⚡ Producție", "💡 Consum", "⚖️ Comparație Producție-Consum"]
)

st.sidebar.markdown("---")

# ==================== ANALIZĂ SURSE DE ENERGIE ====================
if tip_analiza == "📊 Surse de Energie":
    st.header("📊 Analiza Surselor de Energie")

    col1, col2 = st.sidebar.columns(2)

    # Selectare surse
    surse_disponibile = ["carbune", "hidro", "hidrocarburi", "nuclear", "eolian", "fotovolt", "biomasa"]
    surse_selectate = st.sidebar.multiselect(
        "Selectează sursele de energie:",
        surse_disponibile,
        default=["eolian", "fotovolt", "hidro"]
    )

    # Selectare an
    an_selectat = st.sidebar.selectbox("Selectează anul:", [2024, 2025])

    # Selectare granularitate
    granularitate = st.sidebar.radio(
        "Granularitate date:",
        ["Orar", "Zilnic", "Lunar"]
    )

    if surse_selectate:
        # Filtrare date
        df_filtrat = df[df["an"] == an_selectat].copy()

        # Agregare în funcție de granularitate
        if granularitate == "Orar":
            df_agregat = df_filtrat.groupby("ora")[surse_selectate].mean()
            x_label = "Ora"
            x_ticks = range(0, 24)
            x_labels = [f"{h}:00" for h in range(0, 24)]
            titlu = f"Producție medie orară - {an_selectat}"
        elif granularitate == "Zilnic":
            df_filtrat["zi_an"] = df_filtrat["date"].dt.dayofyear
            df_agregat = df_filtrat.groupby("zi_an")[surse_selectate].sum()
            x_label = "Ziua anului"
            x_ticks = None
            x_labels = None
            titlu = f"Producție zilnică - {an_selectat}"
        else:  # Lunar
            df_agregat = df_filtrat.groupby("luna")[surse_selectate].sum()
            x_label = "Luna"
            x_ticks = range(1, 13)
            x_labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec']
            titlu = f"Producție lunară - {an_selectat}"

        # Creare grafic
        fig, ax = plt.subplots(figsize=(14, 7))

        culori = {
            "carbune": "#4a4a4a",
            "hidro": "#2196F3",
            "hidrocarburi": "#795548",
            "nuclear": "#9C27B0",
            "eolian": "#00BCD4",
            "fotovolt": "#FFC107",
            "biomasa": "#4CAF50"
        }

        for sursa in surse_selectate:
            ax.plot(df_agregat.index, df_agregat[sursa],
                    label=sursa.capitalize(), linewidth=2.5,
                    marker='o', markersize=6, color=culori[sursa], alpha=0.8)

        ax.set_xlabel(x_label, fontsize=13, fontweight='bold')
        ax.set_ylabel("Energie (MWh)", fontsize=13, fontweight='bold')
        ax.set_title(titlu, fontsize=15, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        ax.grid(alpha=0.3, linestyle='--', linewidth=0.7)

        if x_ticks is not None:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, rotation=45 if granularitate == "Orar" else 0)

        plt.tight_layout()
        st.pyplot(fig)

        # Statistici
        st.subheader("📈 Statistici Surse Selectate")
        col1, col2, col3 = st.columns(3)

        for i, sursa in enumerate(surse_selectate[:3]):
            total = df_filtrat[sursa].sum()
            medie = df_filtrat[sursa].mean()
            with [col1, col2, col3][i]:
                st.metric(
                    label=f"💡 {sursa.capitalize()}",
                    value=f"{total:,.0f} MWh",
                    delta=f"Medie: {medie:.1f} MWh"
                )
    else:
        st.warning("⚠️ Te rog să selectezi cel puțin o sursă de energie!")

# ==================== ANALIZĂ PRODUCȚIE ====================
elif tip_analiza == "⚡ Producție":
    st.header("⚡ Analiza Producției Totale")

    # Selectare an
    an_selectat = st.sidebar.selectbox("Selectează anul:", [2024, 2025, "Ambii ani"])

    # Selectare granularitate
    granularitate = st.sidebar.radio(
        "Granularitate date:",
        ["Orar", "Zilnic", "Lunar"]
    )

    if an_selectat == "Ambii ani":
        # Comparație între ani
        df_2024 = df[df["an"] == 2024].copy()
        df_2025 = df[df["an"] == 2025].copy()

        if granularitate == "Orar":
            df_2024_ag = df_2024.groupby("ora")["productie"].mean()
            df_2025_ag = df_2025.groupby("ora")["productie"].mean()
            x_label = "Ora"
            x_ticks = range(0, 24)
            x_labels = [f"{h}:00" for h in range(0, 24)]
        elif granularitate == "Zilnic":
            df_2024["zi_an"] = df_2024["date"].dt.dayofyear
            df_2025["zi_an"] = df_2025["date"].dt.dayofyear
            df_2024_ag = df_2024.groupby("zi_an")["productie"].sum()
            df_2025_ag = df_2025.groupby("zi_an")["productie"].sum()
            x_label = "Ziua anului"
            x_ticks = None
            x_labels = None
        else:  # Lunar
            df_2024_ag = df_2024.groupby("luna")["productie"].sum()
            df_2025_ag = df_2025.groupby("luna")["productie"].sum()
            x_label = "Luna"
            x_ticks = range(1, 13)
            x_labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec']

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.fill_between(df_2024_ag.index, 0, df_2024_ag.values,
                        color="#4ECDC4", alpha=0.5, label="Producție 2024")
        ax.plot(df_2024_ag.index, df_2024_ag.values,
                color="#008B8B", linewidth=2.5, marker='o', markersize=7)

        ax.fill_between(df_2025_ag.index, 0, df_2025_ag.values,
                        color="#90EE90", alpha=0.5, label="Producție 2025")
        ax.plot(df_2025_ag.index, df_2025_ag.values,
                color="#228B22", linewidth=2.5, marker='s', markersize=7)

        ax.set_xlabel(x_label, fontsize=13, fontweight='bold')
        ax.set_ylabel("Producție (MWh)", fontsize=13, fontweight='bold')
        ax.set_title(f"Comparație Producție {granularitate}: 2024 vs 2025", fontsize=15, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=12)
        ax.grid(alpha=0.3, linestyle='--', linewidth=0.7)
        ax.set_ylim(bottom=0)

        if x_ticks is not None:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, rotation=45 if granularitate == "Orar" else 0)

        plt.tight_layout()
        st.pyplot(fig)

        # Statistici comparative
        st.subheader("📊 Comparație Statistici")
        col1, col2 = st.columns(2)

        total_2024 = df_2024["productie"].sum()
        total_2025 = df_2025["productie"].sum()
        diferenta = total_2025 - total_2024
        procent = (diferenta / total_2024) * 100

        with col1:
            st.metric("⚡ Total Producție 2024", f"{total_2024:,.0f} MWh")
        with col2:
            st.metric("⚡ Total Producție 2025", f"{total_2025:,.0f} MWh",
                      delta=f"{diferenta:+,.0f} MWh ({procent:+.1f}%)")

    else:
        # Un singur an
        df_filtrat = df[df["an"] == an_selectat].copy()

        if granularitate == "Orar":
            df_agregat = df_filtrat.groupby("ora")["productie"].mean()
            x_label = "Ora"
            x_ticks = range(0, 24)
            x_labels = [f"{h}:00" for h in range(0, 24)]
            titlu = f"Producție medie orară - {an_selectat}"
        elif granularitate == "Zilnic":
            df_filtrat["zi_an"] = df_filtrat["date"].dt.dayofyear
            df_agregat = df_filtrat.groupby("zi_an")["productie"].sum()
            x_label = "Ziua anului"
            x_ticks = None
            x_labels = None
            titlu = f"Producție zilnică - {an_selectat}"
        else:  # Lunar
            df_agregat = df_filtrat.groupby("luna")["productie"].sum()
            x_label = "Luna"
            x_ticks = range(1, 13)
            x_labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec']
            titlu = f"Producție lunară - {an_selectat}"

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.fill_between(df_agregat.index, 0, df_agregat.values,
                        color="#4ECDC4", alpha=0.7)
        ax.plot(df_agregat.index, df_agregat.values,
                color="#008B8B", linewidth=2.5, marker='o', markersize=7)

        ax.set_xlabel(x_label, fontsize=13, fontweight='bold')
        ax.set_ylabel("Producție (MWh)", fontsize=13, fontweight='bold')
        ax.set_title(titlu, fontsize=15, fontweight='bold', pad=20)
        ax.grid(alpha=0.3, linestyle='--', linewidth=0.7)
        ax.set_ylim(bottom=0)

        if x_ticks is not None:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, rotation=45 if granularitate == "Orar" else 0)

        plt.tight_layout()
        st.pyplot(fig)

        # Statistici
        total = df_filtrat["productie"].sum()
        medie = df_filtrat["productie"].mean()
        maxim = df_filtrat["productie"].max()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Producție", f"{total:,.0f} MWh")
        with col2:
            st.metric("📈 Producție Medie", f"{medie:.1f} MWh")
        with col3:
            st.metric("🔝 Producție Maximă", f"{maxim:,.0f} MWh")

# ==================== ANALIZĂ CONSUM ====================
elif tip_analiza == "💡 Consum":
    st.header("💡 Analiza Consumului Total")

    # Selectare an
    an_selectat = st.sidebar.selectbox("Selectează anul:", [2024, 2025, "Ambii ani"])

    # Selectare granularitate
    granularitate = st.sidebar.radio(
        "Granularitate date:",
        ["Orar", "Zilnic", "Lunar"]
    )

    if an_selectat == "Ambii ani":
        # Comparație între ani
        df_2024 = df[df["an"] == 2024].copy()
        df_2025 = df[df["an"] == 2025].copy()

        if granularitate == "Orar":
            df_2024_ag = df_2024.groupby("ora")["consum"].mean()
            df_2025_ag = df_2025.groupby("ora")["consum"].mean()
            x_label = "Ora"
            x_ticks = range(0, 24)
            x_labels = [f"{h}:00" for h in range(0, 24)]
        elif granularitate == "Zilnic":
            df_2024["zi_an"] = df_2024["date"].dt.dayofyear
            df_2025["zi_an"] = df_2025["date"].dt.dayofyear
            df_2024_ag = df_2024.groupby("zi_an")["consum"].sum()
            df_2025_ag = df_2025.groupby("zi_an")["consum"].sum()
            x_label = "Ziua anului"
            x_ticks = None
            x_labels = None
        else:  # Lunar
            df_2024_ag = df_2024.groupby("luna")["consum"].sum()
            df_2025_ag = df_2025.groupby("luna")["consum"].sum()
            x_label = "Luna"
            x_ticks = range(1, 13)
            x_labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec']

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.fill_between(df_2024_ag.index, 0, df_2024_ag.values,
                        color="#FF6B6B", alpha=0.5, label="Consum 2024")
        ax.plot(df_2024_ag.index, df_2024_ag.values,
                color="#CC0000", linewidth=2.5, marker='o', markersize=7)

        ax.fill_between(df_2025_ag.index, 0, df_2025_ag.values,
                        color="#FFA500", alpha=0.5, label="Consum 2025")
        ax.plot(df_2025_ag.index, df_2025_ag.values,
                color="#FF6500", linewidth=2.5, marker='s', markersize=7)

        ax.set_xlabel(x_label, fontsize=13, fontweight='bold')
        ax.set_ylabel("Consum (MWh)", fontsize=13, fontweight='bold')
        ax.set_title(f"Comparație Consum {granularitate}: 2024 vs 2025", fontsize=15, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=12)
        ax.grid(alpha=0.3, linestyle='--', linewidth=0.7)
        ax.set_ylim(bottom=0)

        if x_ticks is not None:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, rotation=45 if granularitate == "Orar" else 0)

        plt.tight_layout()
        st.pyplot(fig)

        # Statistici comparative
        st.subheader("📊 Comparație Statistici")
        col1, col2 = st.columns(2)

        total_2024 = df_2024["consum"].sum()
        total_2025 = df_2025["consum"].sum()
        diferenta = total_2025 - total_2024
        procent = (diferenta / total_2024) * 100

        with col1:
            st.metric("💡 Total Consum 2024", f"{total_2024:,.0f} MWh")
        with col2:
            st.metric("💡 Total Consum 2025", f"{total_2025:,.0f} MWh",
                      delta=f"{diferenta:+,.0f} MWh ({procent:+.1f}%)")

    else:
        # Un singur an
        df_filtrat = df[df["an"] == an_selectat].copy()

        if granularitate == "Orar":
            df_agregat = df_filtrat.groupby("ora")["consum"].mean()
            x_label = "Ora"
            x_ticks = range(0, 24)
            x_labels = [f"{h}:00" for h in range(0, 24)]
            titlu = f"Consum mediu orar - {an_selectat}"
        elif granularitate == "Zilnic":
            df_filtrat["zi_an"] = df_filtrat["date"].dt.dayofyear
            df_agregat = df_filtrat.groupby("zi_an")["consum"].sum()
            x_label = "Ziua anului"
            x_ticks = None
            x_labels = None
            titlu = f"Consum zilnic - {an_selectat}"
        else:  # Lunar
            df_agregat = df_filtrat.groupby("luna")["consum"].sum()
            x_label = "Luna"
            x_ticks = range(1, 13)
            x_labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec']
            titlu = f"Consum lunar - {an_selectat}"

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.fill_between(df_agregat.index, 0, df_agregat.values,
                        color="#FF6B6B", alpha=0.7)
        ax.plot(df_agregat.index, df_agregat.values,
                color="#CC0000", linewidth=2.5, marker='o', markersize=7)

        ax.set_xlabel(x_label, fontsize=13, fontweight='bold')
        ax.set_ylabel("Consum (MWh)", fontsize=13, fontweight='bold')
        ax.set_title(titlu, fontsize=15, fontweight='bold', pad=20)
        ax.grid(alpha=0.3, linestyle='--', linewidth=0.7)
        ax.set_ylim(bottom=0)

        if x_ticks is not None:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, rotation=45 if granularitate == "Orar" else 0)

        plt.tight_layout()
        st.pyplot(fig)

        # Statistici
        total = df_filtrat["consum"].sum()
        medie = df_filtrat["consum"].mean()
        maxim = df_filtrat["consum"].max()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Consum", f"{total:,.0f} MWh")
        with col2:
            st.metric("📈 Consum Mediu", f"{medie:.1f} MWh")
        with col3:
            st.metric("🔝 Consum Maxim", f"{maxim:,.0f} MWh")

# ==================== COMPARAȚIE PRODUCȚIE-CONSUM ====================
else:  # Comparație Producție-Consum
    st.header("⚖️ Comparație Producție vs Consum")

    # Selectare an
    an_selectat = st.sidebar.selectbox("Selectează anul:", [2024, 2025, "Ambii ani"])

    # Selectare granularitate
    granularitate = st.sidebar.radio(
        "Granularitate date:",
        ["Orar", "Zilnic", "Lunar"]
    )

    if an_selectat == "Ambii ani":
        # Comparație pe ambii ani
        df_2024 = df[df["an"] == 2024].copy()
        df_2025 = df[df["an"] == 2025].copy()

        if granularitate == "Lunar":
            df_2024_ag = df_2024.groupby("luna")[["consum", "productie"]].sum()
            df_2025_ag = df_2025.groupby("luna")[["consum", "productie"]].sum()
            x_label = "Luna"
            x_ticks = range(1, 13)
            x_labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec']
        elif granularitate == "Orar":
            df_2024_ag = df_2024.groupby("ora")[["consum", "productie"]].mean()
            df_2025_ag = df_2025.groupby("ora")[["consum", "productie"]].mean()
            x_label = "Ora"
            x_ticks = range(0, 24)
            x_labels = [f"{h}:00" for h in range(0, 24)]
        else:  # Zilnic
            df_2024["zi_an"] = df_2024["date"].dt.dayofyear
            df_2025["zi_an"] = df_2025["date"].dt.dayofyear
            df_2024_ag = df_2024.groupby("zi_an")[["consum", "productie"]].sum()
            df_2025_ag = df_2025.groupby("zi_an")[["consum", "productie"]].sum()
            x_label = "Ziua anului"
            x_ticks = None
            x_labels = None

        fig, axes = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

        # Grafic Consum
        axes[0].fill_between(df_2024_ag.index, 0, df_2024_ag["consum"],
                             color="#FF6B6B", alpha=0.5, label="Consum 2024")
        axes[0].plot(df_2024_ag.index, df_2024_ag["consum"],
                     color="#CC0000", linewidth=2, marker='o', markersize=6)

        axes[0].fill_between(df_2025_ag.index, 0, df_2025_ag["consum"],
                             color="#FFA500", alpha=0.5, label="Consum 2025")
        axes[0].plot(df_2025_ag.index, df_2025_ag["consum"],
                     color="#FF6500", linewidth=2, marker='s', markersize=6)

        axes[0].set_ylabel("Consum (MWh)", fontsize=12, fontweight='bold')
        axes[0].set_title(f"Comparație Consum {granularitate}: 2024 vs 2025", fontsize=13, fontweight='bold')
        axes[0].legend(loc='upper left', fontsize=11)
        axes[0].grid(alpha=0.3, linestyle='--', linewidth=0.7)
        axes[0].set_ylim(bottom=0)

        # Grafic Producție
        axes[1].fill_between(df_2024_ag.index, 0, df_2024_ag["productie"],
                             color="#4ECDC4", alpha=0.5, label="Producție 2024")
        axes[1].plot(df_2024_ag.index, df_2024_ag["productie"],
                     color="#008B8B", linewidth=2, marker='o', markersize=6)

        axes[1].fill_between(df_2025_ag.index, 0, df_2025_ag["productie"],
                             color="#90EE90", alpha=0.5, label="Producție 2025")
        axes[1].plot(df_2025_ag.index, df_2025_ag["productie"],
                     color="#228B22", linewidth=2, marker='s', markersize=6)

        axes[1].set_xlabel(x_label, fontsize=12, fontweight='bold')
        axes[1].set_ylabel("Producție (MWh)", fontsize=12, fontweight='bold')
        axes[1].set_title(f"Comparație Producție {granularitate}: 2024 vs 2025", fontsize=13, fontweight='bold')
        axes[1].legend(loc='upper left', fontsize=11)
        axes[1].grid(alpha=0.3, linestyle='--', linewidth=0.7)
        axes[1].set_ylim(bottom=0)

        if x_ticks is not None:
            axes[1].set_xticks(x_ticks)
            axes[1].set_xticklabels(x_labels, rotation=45 if granularitate == "Orar" else 0)

        plt.suptitle("Comparare anuală: Consum și Producție (2024 vs 2025)",
                     fontsize=15, fontweight='bold', y=0.995)
        plt.tight_layout()
        st.pyplot(fig)

        # Statistici Sold
        st.subheader("⚖️ Bilanț Energetic")
        col1, col2, col3, col4 = st.columns(4)

        sold_2024 = df_2024["sold"].sum()
        sold_2025 = df_2025["sold"].sum()

        with col1:
            st.metric("💡 Consum 2024", f"{df_2024['consum'].sum():,.0f} MWh")
        with col2:
            st.metric("⚡ Producție 2024", f"{df_2024['productie'].sum():,.0f} MWh")
        with col3:
            st.metric("💡 Consum 2025", f"{df_2025['consum'].sum():,.0f} MWh")
        with col4:
            st.metric("⚡ Producție 2025", f"{df_2025['productie'].sum():,.0f} MWh")

        col1, col2 = st.columns(2)
        with col1:
            culoare_2024 = "🟢" if sold_2024 >= 0 else "🔴"
            st.metric(f"{culoare_2024} Sold 2024", f"{sold_2024:+,.0f} MWh")
        with col2:
            culoare_2025 = "🟢" if sold_2025 >= 0 else "🔴"
            st.metric(f"{culoare_2025} Sold 2025", f"{sold_2025:+,.0f} MWh")

    else:
        # Un singur an
        df_filtrat = df[df["an"] == an_selectat].copy()

        if granularitate == "Orar":
            df_agregat = df_filtrat.groupby("ora")[["consum", "productie"]].mean()
            x_label = "Ora"
            x_ticks = range(0, 24)
            x_labels = [f"{h}:00" for h in range(0, 24)]
        elif granularitate == "Zilnic":
            df_filtrat["zi_an"] = df_filtrat["date"].dt.dayofyear
            df_agregat = df_filtrat.groupby("zi_an")[["consum", "productie"]].sum()
            x_label = "Ziua anului"
            x_ticks = None
            x_labels = None
        else:  # Lunar
            df_agregat = df_filtrat.groupby("luna")[["consum", "productie"]].sum()
            x_label = "Luna"
            x_ticks = range(1, 13)
            x_labels = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun', 'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec']

        fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Grafic Consum
        axes[0].fill_between(df_agregat.index, 0, df_agregat["consum"],
                             color="#FF6B6B", alpha=0.7, label="Consum")
        axes[0].plot(df_agregat.index, df_agregat["consum"],
                     color="#CC0000", linewidth=2.5, alpha=0.9, marker='o', markersize=7)

        axes[0].set_ylabel("Consum (MWh)", fontsize=12, fontweight='bold')
        axes[0].set_title(f"Evoluția consumului - {an_selectat}", fontsize=13, fontweight='bold')
        axes[0].legend(loc='upper left', fontsize=11)
        axes[0].grid(alpha=0.3, linestyle='--', linewidth=0.7)
        axes[0].set_ylim(bottom=0)

        # Grafic Producție
        axes[1].fill_between(df_agregat.index, 0, df_agregat["productie"],
                             color="#4ECDC4", alpha=0.7, label="Producție")
        axes[1].plot(df_agregat.index, df_agregat["productie"],
                     color="#008B8B", linewidth=2.5, alpha=0.9, marker='o', markersize=7)

        axes[1].set_xlabel(x_label, fontsize=12, fontweight='bold')
        axes[1].set_ylabel("Producție (MWh)", fontsize=12, fontweight='bold')
        axes[1].set_title(f"Evoluția producției - {an_selectat}", fontsize=13, fontweight='bold')
        axes[1].legend(loc='upper left', fontsize=11)
        axes[1].grid(alpha=0.3, linestyle='--', linewidth=0.7)
        axes[1].set_ylim(bottom=0)

        if x_ticks is not None:
            axes[1].set_xticks(x_ticks)
            axes[1].set_xticklabels(x_labels, rotation=45 if granularitate == "Orar" else 0)

        plt.suptitle(f"Comparare Consum și Producție - {an_selectat} ({granularitate})",
                     fontsize=15, fontweight='bold', y=0.995)
        plt.tight_layout()
        st.pyplot(fig)

        # Statistici
        total_consum = df_filtrat["consum"].sum()
        total_productie = df_filtrat["productie"].sum()
        sold = df_filtrat["sold"].sum()

        st.subheader("📊 Statistici Generale")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💡 Total Consum", f"{total_consum:,.0f} MWh")
        with col2:
            st.metric("⚡ Total Producție", f"{total_productie:,.0f} MWh")
        with col3:
            culoare = "🟢" if sold >= 0 else "🔴"
            st.metric(f"{culoare} Sold Energetic", f"{sold:+,.0f} MWh")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>📊 Dashboard Energie România | Dezvoltat cu Streamlit & Python</p>
        <p>Date actualizate: 2024-2025</p>
    </div>
""", unsafe_allow_html=True)
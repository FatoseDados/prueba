
import streamlit as st
import pandas as pd
import altair as alt

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Fatos&Dados", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f7f9fa;
        }
        .block-container {
            padding: 2rem 2rem 1rem 2rem;
        }
        h1, h2 {
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# --- Selector de idioma ---
lang = st.sidebar.radio("Idioma / Language", ["🇺🇾 Español", "🇧🇷 Português"])

# --- Diccionario de traducción ---
T = {
    "es": {
        "title_public": "📢 Panel Público de Resultados",
        "title_private": "📊 Panel Interno de Análisis",
        "desc": "Resumen general de las encuestas disponibles.",
        "voto": "Intención de voto",
        "satisfaccion": "Satisfacción general",
        "problema": "Principal preocupación de la población",
        "datos": "Datos crudos",
        "voto_ciudad": "Intención de voto por ciudad",
        "problema_mencionado": "Principal problema mencionado"
    },
    "pt": {
        "title_public": "📢 Painel Público de Resultados",
        "title_private": "📊 Painel Interno de Análise",
        "desc": "Resumo geral das pesquisas disponíveis.",
        "voto": "Intenção de voto",
        "satisfaccion": "Satisfação geral",
        "problema": "Principal preocupação da população",
        "datos": "Dados brutos",
        "voto_ciudad": "Intenção de voto por cidade",
        "problema_mencionado": "Principal problema mencionado"
    }
}

idioma = "es" if lang == "🇺🇾 Español" else "pt"

# --- CARGAR DATOS ---
SHEET_ID = "1wvG8-f4pAi5VygAqsvL7GZ6DCQbB0uVUfL1IXj6j5iA"
SHEET_NAME = "Hoja1"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

st.title(T[idioma]["title_public"])
st.markdown(T[idioma]["desc"])

try:
    df = pd.read_csv(url)

    st.subheader("📊 " + T[idioma]["voto"])
    if "p6" in df.columns:
        voto = df["p6"].value_counts(normalize=True).reset_index()
        voto.columns = ["Candidato", "Porcentaje"]
        voto["Porcentaje"] = (voto["Porcentaje"] * 100).round(2)
        chart = alt.Chart(voto).mark_bar().encode(
            x="Candidato:N", y="Porcentaje:Q", color="Candidato:N",
            tooltip=["Candidato", "Porcentaje"]
        ).properties(width=700, height=400)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("😊 " + T[idioma]["satisfaccion"])
    if "p7" in df.columns:
        satis = df["p7"].value_counts(normalize=True).reset_index()
        satis.columns = ["Nivel", "Porcentaje"]
        satis["Porcentaje"] = (satis["Porcentaje"] * 100).round(2)
        pie = alt.Chart(satis).mark_arc(innerRadius=50).encode(
            theta="Porcentaje:Q", color="Nivel:N", tooltip=["Nivel", "Porcentaje"]
        ).properties(width=400, height=400)
        st.altair_chart(pie)

    if "p8" in df.columns:
        problema = df["p8"].value_counts().idxmax()
        st.info(f"🔍 {T[idioma]['problema']}: **{problema}**")

except Exception as e:
    st.error("Error al cargar datos desde Google Sheets.")
    st.code(str(e))

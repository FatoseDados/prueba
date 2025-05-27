import streamlit as st
import pandas as pd
import altair as alt

# --- CSS personalizado ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f7f9fa;
        }

        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
        }

        h1, h2, h3 {
            color: #0e1117;
        }

        .metric-box {
            background-color: #ffffff;
            padding: 1rem 2rem;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            border-left: 5px solid #3a86ff;
        }

        .metric-title {
            color: #6c757d;
            font-size: 16px;
        }

        .metric-value {
            color: #212529;
            font-size: 32px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Análisis Político en Tiempo Real", layout="wide")
st.title("📊 Panel de Análisis Político")
st.markdown("Datos en vivo de encuestas a través de KoBoToolbox conectadas con Google Sheets.")

# --- URL DE GOOGLE SHEETS ---
SHEET_ID = "1wvG8-f4pAi5VygAqsvL7GZ6DCQbB0uVUfL1IXj6j5iA"
SHEET_NAME = "Hoja1"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# --- LECTURA DE DATOS ---
try:
    df = pd.read_csv(url)
    st.subheader("📋 Datos Brutos")
    st.dataframe(df)

    total = len(df)

    # --- Métrica: total encuestas ---
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Encuestas recibidas</div>
            <div class="metric-value">{total}</div>
        </div>
    """, unsafe_allow_html=True)

    # --- INTENCIÓN DE VOTO ---
    if "p6" in df.columns:
        voto = df["p6"].value_counts(normalize=True).reset_index()
        voto.columns = ["Candidato", "Porcentaje"]
        voto["Porcentaje"] = (voto["Porcentaje"] * 100).round(2)

        st.subheader("🗳️ Intención de Voto General")
        st.dataframe(voto)

        chart_voto = alt.Chart(voto).mark_bar().encode(
            x="Candidato:N",
            y="Porcentaje:Q",
            color="Candidato:N",
            tooltip=["Candidato", "Porcentaje"]
        ).properties(width=600, height=400)

        st.altair_chart(chart_voto, use_container_width=True)

    # --- SATISFACCIÓN ---
    if "p7" in df.columns:
        satis = df["p7"].value_counts(normalize=True).reset_index()
        satis.columns = ["Satisfacción", "Porcentaje"]
        satis["Porcentaje"] = (satis["Porcentaje"] * 100).round(2)

        st.subheader("📈 Nivel de Satisfacción con el Gobierno")
        st.dataframe(satis)

        chart_satis = alt.Chart(satis).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Porcentaje", type="quantitative"),
            color=alt.Color(field="Satisfacción", type="nominal"),
            tooltip=["Satisfacción", "Porcentaje"]
        ).properties(width=400, height=400)

        st.altair_chart(chart_satis)

    # --- PROYECCIÓN SIMPLE: Candidato más votado ---
    if "p6" in df.columns:
        mayor_candidato = df["p6"].value_counts().idxmax()
        porcentaje = (df["p6"].value_counts(normalize=True).max() * 100).round(2)

        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Candidato más votado</div>
                <div class="metric-value">{mayor_candidato} ({porcentaje}%)</div>
            </div>
        """, unsafe_allow_html=True)

    # --- PROBLEMA SOCIAL PRINCIPAL ---
    if "p8" in df.columns:
        mayor_problema = df["p8"].value_counts().idxmax()

        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Problema principal mencionado</div>
                <div class="metric-value">{mayor_problema}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- GRÁFICO POR CIUDAD Y CANDIDATO ---
    if "p1" in df.columns and "p6" in df.columns:
        conteo = df.groupby(["p1", "p6"]).size().reset_index(name="Cantidad")
        chart = alt.Chart(conteo).mark_bar().encode(
            x='p1:N',
            y='Cantidad:Q',
            color='p6:N',
            tooltip=['p1', 'p6', 'Cantidad']
        ).properties(width=700, height=400)

        st.subheader("🏙️ Intención de voto por ciudad")
        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error("❌ Error al cargar datos desde Google Sheets.")
    st.code(str(e))

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Panel Público - Fatos&Dados", layout="wide")
st.title("📢 Panel Público de Resultados")
st.markdown("Resumen general de las encuestas disponibles.")

# Cargar datos desde Google Sheets
SHEET_ID = "1wvG8-f4pAi5VygAqsvL7GZ6DCQbB0uVUfL1IXj6j5iA"
SHEET_NAME = "Hoja1"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    df = pd.read_csv(url)

    st.subheader("📊 Intención de voto")
    if "p6" in df.columns:
        voto = df["p6"].value_counts(normalize=True).reset_index()
        voto.columns = ["Candidato", "Porcentaje"]
        voto["Porcentaje"] = (voto["Porcentaje"] * 100).round(2)
        chart = alt.Chart(voto).mark_bar().encode(
            x="Candidato:N", y="Porcentaje:Q", color="Candidato:N",
            tooltip=["Candidato", "Porcentaje"]
        ).properties(width=700, height=400)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("😊 Satisfacción general")
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
        st.info(f"🔍 Principal preocupación de la población: **{problema}**")

except Exception as e:
    st.error("Error al cargar datos desde Google Sheets.")
    st.code(str(e))

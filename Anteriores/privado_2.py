import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Panel Interno - Fatos&Dados", layout="wide")
st.title("📊 Panel Interno de Análisis")
st.markdown("Datos completos y detallados provenientes de encuestas.")

# Cargar datos desde Google Sheets
SHEET_ID = "1wvG8-f4pAi5VygAqsvL7GZ6DCQbB0uVUfL1IXj6j5iA"
SHEET_NAME = "Hoja1"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    df = pd.read_csv(url)
    st.subheader("📋 Datos crudos")
    st.dataframe(df)

    st.subheader("🗳️ Intención de voto")
    if "p6" in df.columns:
        voto = df["p6"].value_counts(normalize=True).reset_index()
        voto.columns = ["Candidato", "Porcentaje"]
        voto["Porcentaje"] = (voto["Porcentaje"] * 100).round(2)
        st.dataframe(voto)
        chart = alt.Chart(voto).mark_bar().encode(
            x="Candidato:N", y="Porcentaje:Q", color="Candidato:N",
            tooltip=["Candidato", "Porcentaje"]
        ).properties(width=700, height=400)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("📈 Satisfacción ciudadana")
    if "p7" in df.columns:
        satis = df["p7"].value_counts(normalize=True).reset_index()
        satis.columns = ["Nivel", "Porcentaje"]
        satis["Porcentaje"] = (satis["Porcentaje"] * 100).round(2)
        st.dataframe(satis)
        pie = alt.Chart(satis).mark_arc(innerRadius=50).encode(
            theta="Porcentaje:Q", color="Nivel:N", tooltip=["Nivel", "Porcentaje"]
        ).properties(width=400, height=400)
        st.altair_chart(pie)

    st.subheader("🏙️ Intención de voto por ciudad")
    if "p1" in df.columns and "p6" in df.columns:
        resumen = df.groupby(["p1", "p6"]).size().reset_index(name="Cantidad")
        st.dataframe(resumen)
        chart2 = alt.Chart(resumen).mark_bar().encode(
            x="p1:N", y="Cantidad:Q", color="p6:N", tooltip=["p1", "p6", "Cantidad"]
        ).properties(width=700, height=400)
        st.altair_chart(chart2, use_container_width=True)

    if "p8" in df.columns:
        problema = df["p8"].value_counts().idxmax()
        st.success(f"✅ Principal problema mencionado: **{problema}**")

except Exception as e:
    st.error("Error al cargar datos desde Google Sheets.")
    st.code(str(e))

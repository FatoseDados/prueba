import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Análisis Electoral", layout="wide")

st.title("📊 Análisis Electoral Integrado")
st.markdown("Panel generado con datos unificados desde múltiples encuestas de KoBoToolbox.")

# Carga de datos desde Google Sheets
SHEET_ID = "1F6L7myGDcz2_fDpsQEhdIZfj268KTWy1-3uvHUSO53c"
SHEET_NAME = "DatosMaestros"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    df["p2"] = pd.to_numeric(df["p2"], errors="coerce")
    df.dropna(subset=["p2"], inplace=True)

    # Clasificación por edad
    def clasificar_edad(edad):
        if edad < 30:
            return "18-29"
        elif edad < 45:
            return "30-44"
        elif edad < 60:
            return "45-59"
        else:
            return "60+"

    df["RangoEdad"] = df["p2"].apply(clasificar_edad)

    # Candidatos, géneros, edades
    candidatos = sorted(df["p4"].dropna().unique())
    generos_disponibles = sorted(df["p3"].dropna().unique())
    rangos_disponibles = sorted(df["RangoEdad"].dropna().unique())
    ciudades_disponibles = sorted(df["Ciudad"].dropna().unique())

    # Filtro de ciudad
    st.sidebar.header("Filtros")
    ciudad_sel = st.sidebar.selectbox("Ciudad", ["Todas"] + ciudades_disponibles)

    if ciudad_sel != "Todas":
        df = df[df["Ciudad"] == ciudad_sel]
        st.markdown(f"📍 Mostrando datos para **{ciudad_sel}**")
    else:
        st.markdown("🌐 Mostrando datos a nivel **nacional**")

    st.markdown(f"🗂️ Total de encuestas: **{len(df)}**")

    # KPIs generales
    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Candidatos", len(candidatos))
    col2.metric("🧑‍🤝‍🧑 Géneros", len(generos_disponibles))
    col3.metric("🏙️ Ciudades", len(ciudades_disponibles))

    # --- Distribución por rango etario
    st.subheader("📊 Distribución de votantes por rango de edad")
    edades = df["RangoEdad"].value_counts().reset_index()
    edades.columns = ["Rango de Edad", "Cantidad"]
    edades["Porcentaje"] = ((edades["Cantidad"] / edades["Cantidad"].sum()) * 100).round(2)
    st.altair_chart(
        alt.Chart(edades).mark_bar().encode(
            x="Rango de Edad",
            y="Cantidad",
            color="Rango de Edad",
            tooltip=["Rango de Edad", "Cantidad", "Porcentaje"]
        ).properties(width=600),
        use_container_width=True
    )

    # --- Distribución por género
    st.subheader("🧍 Distribución de votantes por género")
    genero = df["p3"].value_counts().reset_index()
    genero.columns = ["Género", "Cantidad"]
    genero["Porcentaje"] = ((genero["Cantidad"] / genero["Cantidad"].sum()) * 100).round(2)
    st.altair_chart(
        alt.Chart(genero).mark_arc(innerRadius=50).encode(
            theta="Cantidad",
            color="Género",
            tooltip=["Género", "Cantidad", "Porcentaje"]
        ).properties(width=400, height=400),
    )

    # --- Intención de voto general
    st.subheader("📌 Intención de voto general")
    voto_total = df["p4"].value_counts().reindex(candidatos, fill_value=0).reset_index()
    voto_total.columns = ["Candidato", "Cantidad"]
    voto_total["Porcentaje"] = ((voto_total["Cantidad"] / voto_total["Cantidad"].sum()) * 100).round(2)
    st.altair_chart(
        alt.Chart(voto_total).mark_bar().encode(
            x="Candidato",
            y="Cantidad",
            color="Candidato",
            tooltip=["Candidato", "Cantidad", "Porcentaje"]
        ).properties(width=700),
        use_container_width=True
    )

    # --- Intención de voto por género
    st.subheader("🗳️ Intención de voto por género")
    genero_sel = st.selectbox("Selecciona un género", generos_disponibles)
    votos_genero = df[df["p3"] == genero_sel]["p4"].value_counts().reindex(candidatos, fill_value=0).reset_index()
    votos_genero.columns = ["Candidato", "Cantidad"]
    st.altair_chart(
        alt.Chart(votos_genero).mark_bar().encode(
            x='Candidato:N',
            y='Cantidad:Q',
            color='Candidato:N',
            tooltip=['Candidato', 'Cantidad']
        ).properties(width=600),
        use_container_width=True
    )

    # --- Intención de voto por rango etario
    st.subheader("📈 Intención de voto por rango de edad")
    edad_sel = st.selectbox("Selecciona un rango de edad", rangos_disponibles)
    votos_edad = df[df["RangoEdad"] == edad_sel]["p4"].value_counts().reindex(candidatos, fill_value=0).reset_index()
    votos_edad.columns = ["Candidato", "Cantidad"]
    st.altair_chart(
        alt.Chart(votos_edad).mark_bar().encode(
            x='Candidato:N',
            y='Cantidad:Q',
            color='Candidato:N',
            tooltip=['Candidato', 'Cantidad']
        ).properties(width=600),
        use_container_width=True
    )

    # --- Satisfacción con el gobierno
    st.subheader("📊 Satisfacción con el gobierno")
    satisf = df["p5"].value_counts().reset_index()
    satisf.columns = ["Satisfacción", "Cantidad"]
    satisf["Porcentaje"] = ((satisf["Cantidad"] / satisf["Cantidad"].sum()) * 100).round(2)
    st.altair_chart(
        alt.Chart(satisf).mark_arc(innerRadius=40).encode(
            theta="Cantidad",
            color="Satisfacción",
            tooltip=["Satisfacción", "Cantidad", "Porcentaje"]
        ).properties(width=400, height=400)
    )

    # --- Principales problemas
    st.subheader("🚨 Principales problemas mencionados")
    problemas = df["p6"].value_counts().reset_index()
    problemas.columns = ["Problema", "Cantidad"]
    st.altair_chart(
        alt.Chart(problemas).mark_bar().encode(
            x="Cantidad:Q",
            y=alt.Y("Problema:N", sort='-x'),
            color="Problema:N",
            tooltip=["Problema", "Cantidad"]
        ).properties(width=700, height=400)
    )

except Exception as e:
    st.error("❌ Error al cargar o procesar los datos.")
    st.code(str(e))

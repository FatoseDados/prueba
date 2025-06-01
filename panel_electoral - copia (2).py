import streamlit as st
import pandas as pd
import altair as alt

# CONFIGURACIÓN
st.set_page_config(page_title="Análisis Electoral", layout="wide")

# ENCABEZADO
st.title("📊 Análisis Electoral Integrado")
st.markdown("Panel generado con datos unificados desde múltiples encuestas de KoBoToolbox.")

# LECTURA DE DATOS
SHEET_ID = "1F6L7myGDcz2_fDpsQEhdIZfj268KTWy1-3uvHUSO53c"
SHEET_NAME = "DatosMaestros"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    df = pd.read_csv(url)

    st.success("Datos cargados correctamente.")
    st.markdown(f"Total de registros: **{len(df)}**")

    # NORMALIZACIÓN DE COLUMNAS
    df.columns = df.columns.str.strip()

    # CONVERSIÓN DE EDAD
    df["p2"] = pd.to_numeric(df["p2"], errors="coerce")
    df.dropna(subset=["p2"], inplace=True)

    # RANGO DE EDAD
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

    # 🔹 DISTRIBUCIÓN POR RANGO DE EDAD
    st.subheader("📊 Distribución de votantes por rango de edad")
    edades = df["RangoEdad"].value_counts().reset_index()
    edades.columns = ["Rango de Edad", "Cantidad"]
    edades["Porcentaje"] = (edades["Cantidad"] / edades["Cantidad"].sum() * 100).round(2)
    st.dataframe(edades)

    chart_edad = alt.Chart(edades).mark_bar().encode(
        x=alt.X("Rango de Edad", sort=["18-29", "30-44", "45-59", "60+"]),
        y="Cantidad:Q",
        color="Rango de Edad:N",
        tooltip=["Rango de Edad", "Cantidad", "Porcentaje"]
    ).properties(width=600)
    st.altair_chart(chart_edad, use_container_width=True)

    # 🔹 DISTRIBUCIÓN POR GÉNERO
    st.subheader("🧍 Distribución de votantes por género")
    genero = df["p3"].value_counts().reset_index()
    genero.columns = ["Género", "Cantidad"]
    genero["Porcentaje"] = (genero["Cantidad"] / genero["Cantidad"].sum() * 100).round(2)
    st.dataframe(genero)

    chart_genero = alt.Chart(genero).mark_arc(innerRadius=50).encode(
        theta="Cantidad:Q",
        color="Género:N",
        tooltip=["Género", "Cantidad", "Porcentaje"]
    ).properties(width=400, height=400)
    st.altair_chart(chart_genero)

  # INTENCIÓN DE VOTO POR GÉNERO CON SELECTBOX
    st.subheader("🗳️ Intención de voto por género")

    generos_disponibles = df["p3"].dropna().unique().tolist()
    genero_seleccionado = st.selectbox("Selecciona un género", generos_disponibles, index=0)

    voto_genero_filtrado = df[df["p3"] == genero_seleccionado]
    voto_genero_data = voto_genero_filtrado["p4"].value_counts().reset_index()
    voto_genero_data.columns = ["Candidato", "Cantidad"]

    chart_vg = alt.Chart(voto_genero_data).mark_bar().encode(
        x='Candidato:N',
        y='Cantidad:Q',
        color='Candidato:N',
        tooltip=['Candidato', 'Cantidad']
    ).properties(width=600)

    st.altair_chart(chart_vg, use_container_width=True)


# INTENCIÓN DE VOTO POR RANGO DE EDAD CON SELECTBOX
    st.subheader("📈 Intención de voto por rango de edad")

    rangos_disponibles = df["RangoEdad"].dropna().unique().tolist()
    rango_seleccionado = st.selectbox("Selecciona un rango de edad", rangos_disponibles, index=0)

    voto_edad_filtrado = df[df["RangoEdad"] == rango_seleccionado]
    voto_edad_data = voto_edad_filtrado["p4"].value_counts().reset_index()
    voto_edad_data.columns = ["Candidato", "Cantidad"]

    chart_ve = alt.Chart(voto_edad_data).mark_bar().encode(
        x='Candidato:N',
        y='Cantidad:Q',
        color='Candidato:N',
        tooltip=['Candidato', 'Cantidad']
    ).properties(width=600)

    st.altair_chart(chart_ve, use_container_width=True)


    # 🔹 INTENCIÓN DE VOTO GENERAL
    st.subheader("📌 Intención de voto general")
    voto_total = df["p4"].value_counts().reset_index()
    voto_total.columns = ["Candidato", "Cantidad"]
    voto_total["Porcentaje"] = (voto_total["Cantidad"] / voto_total["Cantidad"].sum() * 100).round(2)
    st.dataframe(voto_total)

    chart_voto = alt.Chart(voto_total).mark_bar().encode(
        x="Candidato:N",
        y="Cantidad:Q",
        color="Candidato:N",
        tooltip=["Candidato", "Cantidad", "Porcentaje"]
    ).properties(width=600)
    st.altair_chart(chart_voto, use_container_width=True)

    # 🔹 SATISFACCIÓN CON EL GOBIERNO
    st.subheader("📊 Satisfacción con el gobierno")
    satisf = df["p5"].value_counts().reset_index()
    satisf.columns = ["Satisfacción", "Cantidad"]
    satisf["Porcentaje"] = (satisf["Cantidad"] / satisf["Cantidad"].sum() * 100).round(2)
    st.dataframe(satisf)

    chart_satis = alt.Chart(satisf).mark_arc(innerRadius=40).encode(
        theta="Cantidad:Q",
        color="Satisfacción:N",
        tooltip=["Satisfacción", "Cantidad", "Porcentaje"]
    ).properties(width=400, height=400)
    st.altair_chart(chart_satis)

    # 🔹 PROBLEMAS PRINCIPALES
    st.subheader("🚨 Principales problemas mencionados")
    problemas = df["p6"].value_counts().reset_index()
    problemas.columns = ["Problema", "Cantidad"]
    st.dataframe(problemas)

    chart_problemas = alt.Chart(problemas).mark_bar().encode(
        x="Cantidad:Q",
        y=alt.Y("Problema:N", sort='-x'),
        color="Problema:N",
        tooltip=["Problema", "Cantidad"]
    ).properties(width=700, height=400)
    st.altair_chart(chart_problemas)

except Exception as e:
    st.error("❌ Error al cargar o procesar los datos.")
    st.code(str(e))

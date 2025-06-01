
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
    st.markdown("Total de registros: **{}**".format(len(df)))

    # CONVERSIÓN DE TIPOS
    df.columns = df.columns.str.strip()
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

    # DISTRIBUCIÓN DE VOTANTES POR EDAD
    st.subheader("📊 Distribución de votantes por rango de edad")
    edades = df["RangoEdad"].value_counts(normalize=True).reset_index()
    edades.columns = ["Rango de Edad", "Porcentaje"]
    edades["Porcentaje"] = (edades["Porcentaje"] * 100).round(2)
    st.dataframe(edades)

    chart_edad = alt.Chart(edades).mark_bar().encode(
        x="Rango de Edad",
        y="Porcentaje",
        color="Rango de Edad",
        tooltip=["Rango de Edad", "Porcentaje"]
    ).properties(width=600)
    st.altair_chart(chart_edad, use_container_width=True)

    # DISTRIBUCIÓN POR GÉNERO
    st.subheader("🧍 Distribución de votantes por género")
    genero = df["p3"].value_counts(normalize=True).reset_index()
    genero.columns = ["Género", "Porcentaje"]
    genero["Porcentaje"] = (genero["Porcentaje"] * 100).round(2)
    st.dataframe(genero)

    chart_genero = alt.Chart(genero).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Porcentaje", type="quantitative"),
        color=alt.Color(field="Género", type="nominal"),
        tooltip=["Género", "Porcentaje"]
    ).properties(width=400, height=400)
    st.altair_chart(chart_genero)

    # INTENCIÓN DE VOTO POR GÉNERO
    st.subheader("🗳️ Intención de voto por género")
    voto_genero = df.groupby(["p3", "p4"]).size().reset_index(name="Cantidad")
    chart_vg = alt.Chart(voto_genero).mark_bar().encode(
        x='p4:N',
        y='Cantidad:Q',
        color='p3:N',
        column='p3:N',
        tooltip=['p3', 'p4', 'Cantidad']
    ).properties(width=160, height=300)
    st.altair_chart(chart_vg, use_container_width=True)

    # INTENCIÓN DE VOTO POR EDAD
    st.subheader("📈 Intención de voto por rango de edad")
    voto_edad = df.groupby(["RangoEdad", "p4"]).size().reset_index(name="Cantidad")
    chart_ve = alt.Chart(voto_edad).mark_bar().encode(
        x='p4:N',
        y='Cantidad:Q',
        color='RangoEdad:N',
        column='RangoEdad:N',
        tooltip=['RangoEdad', 'p4', 'Cantidad']
    ).properties(width=160, height=300)
    st.altair_chart(chart_ve, use_container_width=True)

    # INTENCIÓN DE VOTO GENERAL
    st.subheader("📌 Intención de voto general")
    voto_total = df["p4"].value_counts(normalize=True).reset_index()
    voto_total.columns = ["Candidato", "Porcentaje"]
    voto_total["Porcentaje"] = (voto_total["Porcentaje"] * 100).round(2)
    st.dataframe(voto_total)

    chart_voto = alt.Chart(voto_total).mark_bar().encode(
        x="Candidato",
        y="Porcentaje",
        color="Candidato",
        tooltip=["Candidato", "Porcentaje"]
    ).properties(width=600)
    st.altair_chart(chart_voto, use_container_width=True)

    # NIVEL DE SATISFACCIÓN
    st.subheader("📊 Satisfacción con el gobierno")
    satisf = df["p5"].value_counts(normalize=True).reset_index()
    satisf.columns = ["Satisfacción", "Porcentaje"]
    satisf["Porcentaje"] = (satisf["Porcentaje"] * 100).round(2)
    st.dataframe(satisf)

    chart_satis = alt.Chart(satisf).mark_arc(innerRadius=40).encode(
        theta="Porcentaje",
        color="Satisfacción",
        tooltip=["Satisfacción", "Porcentaje"]
    ).properties(width=400, height=400)
    st.altair_chart(chart_satis)

    # PROBLEMAS PRINCIPALES
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

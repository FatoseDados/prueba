
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Fatos&Dados", layout="wide")
st.markdown('''
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f1f3f6;
    }

    .block-container {
        padding: 2rem 2rem 1rem 2rem;
    }

    h1, h2, h3 {
        color: #1f3b57;
    }

    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .card-title {
        font-size: 18px;
        color: #6c757d;
    }

    .card-value {
        font-size: 28px;
        font-weight: 600;
        color: #2c3e50;
    }
</style>
''', unsafe_allow_html=True)

lang = st.sidebar.radio("🌐 Idioma / Language", ["🇺🇾 Español", "🇧🇷 Português"])

T = {
    "es": {
        "title_public": "📢 Panel Público de Resultados",
        "title_private": "📊 Panel Interno de Análisis",
        "desc": "Visualización de los datos recolectados por Fatos&Dados.",
        "voto": "Intención de voto",
        "satisfaccion": "Satisfacción general",
        "problema": "Principal preocupación",
        "datos": "Datos crudos",
        "voto_ciudad": "Voto por ciudad"
    },
    "pt": {
        "title_public": "📢 Painel Público de Resultados",
        "title_private": "📊 Painel Interno de Análise",
        "desc": "Visualização dos dados coletados pelo Fatos&Dados.",
        "voto": "Intenção de voto",
        "satisfaccion": "Satisfação geral",
        "problema": "Principal preocupação",
        "datos": "Dados brutos",
        "voto_ciudad": "Voto por cidade"
    }
}

idioma = "es" if lang == "🇺🇾 Español" else "pt"

# Leer datos
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

        st.markdown('<div class="card"><div class="card-title">Resumen</div><div class="card-value">' +
                    f"{voto.iloc[0]['Candidato']} ({voto.iloc[0]['Porcentaje']}%)" +
                    '</div></div>', unsafe_allow_html=True)

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
        st.markdown('<div class="card"><div class="card-title">' + T[idioma]["problema"] +
                    '</div><div class="card-value">' + problema + '</div></div>', unsafe_allow_html=True)

except Exception as e:
    st.error("Error al cargar datos desde Google Sheets.")
    st.code(str(e))

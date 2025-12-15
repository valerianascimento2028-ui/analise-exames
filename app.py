import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="Análise de Exames", layout="centered")

st.title("🧪 Análise automática de exames laboratoriais")
st.write("Envie o PDF do exame para análise.")

pdf = st.file_uploader("Enviar PDF do exame", type=["pdf"])

if pdf:
    resultados = []

    with pdfplumber.open(pdf) as arquivo:
        for pagina in arquivo.pages:
            texto = pagina.extract_text()
            if texto:
                linhas = texto.split("\n")
                for linha in linhas:
                    if "Creatinina" in linha:
                        resultados.append({
                            "Exame": "Creatinina",
                            "Resultado": linha,
                            "Referência": "0,53 – 1,00 mg/dL",
                            "Classificação": "Normal"
                        })

    if resultados:
        df = pd.DataFrame(resultados)
        st.dataframe(df)
    else:
        st.warning("Nenhum exame reconhecido no PDF.")

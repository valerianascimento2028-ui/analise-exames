import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="Análise de Exames", layout="centered")

st.title("🧪 Análise automática de exames laboratoriais")
st.write("Envie o PDF do exame para análise.")

pdf = st.file_uploader("Enviar PDF do exame", type=["pdf"])

# Função para classificar
def classificar(valor, minimo, maximo):
    if minimo <= valor <= maximo:
        return "Normal"
    else:
        return "Alterado"

# Função para cor
def colorir(valor):
    if valor == "Normal":
        return "background-color: #c6efce"
    else:
        return "background-color: #ffc7ce"

if pdf:
    resultados = []

    with pdfplumber.open(pdf) as arquivo:
        for pagina in arquivo.pages:
            texto = pagina.extract_text()
            if texto:
                linhas = texto.split("\n")

                for linha in linhas:

                    # CREATININA
                    if "Creatinina" in linha:
                        numeros = re.findall(r"\d+,\d+|\d+\.\d+", linha)
                        if numeros:
                            valor = float(numeros[0].replace(",", "."))
                            classe = classificar(valor, 0.53, 1.00)

                            resultados.append({
                                "Exame": "Creatinina",
                                "Resultado": valor,
                                "Referência": "0,53 – 1,00",
                                "Classificação": classe
                            })

                    # GLICOSE
                    if "Glicose" in linha or "GLICOSE" in linha:
                        numeros = re.findall(r"\d+", linha)
                        if numeros:
                            valor = float(numeros[0])
                            classe = classificar(valor, 70, 99)

                            resultados.append({
                                "Exame": "Glicose",
                                "Resultado": valor,
                                "Referência": "70 – 99",
                                "Classificação": classe
                            })

    if resultados:
        df = pd.DataFrame(resultados)

        st.subheader("📊 Resultados")
        st.dataframe(
            df.style.applymap(colorir, subset=["Classificação"])
        )
    else:
        st.warning("Nenhum exame reconhecido no PDF.")

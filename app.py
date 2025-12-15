import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Extrator de Exames", layout="centered")

st.title("🧪 Extrator de dados de exames laboratoriais")
st.write("Envie o PDF para extrair os valores dos exames.")

pdf = st.file_uploader("Enviar PDF do exame", type=["pdf"])

# Dicionário de exames: nome no PDF → saída padronizada
EXAMES = {
    "HEMOGLOBINA": ("Hb", "g/dL"),
    "HEMATÓCRITO": ("Ht", "%"),
    "LEUCÓCITOS": ("Leu", "/mm³"),
    "PLAQUETAS": ("Plq", "/mm³"),

    "FERRITINA": ("Ferritina", "ng/mL"),
    "ÁCIDO FÓLICO": ("Ácido fólico", "ng/mL"),
    "VITAMINA B12": ("Vitamina B12", "pg/mL"),
    "VITAMINA D": ("Vitamina D", "ng/mL"),

    "CREATININA": ("Creatinina", "mg/dL"),
    "GLICOSE": ("Glicose", "mg/dL"),

    "COLESTEROL TOTAL": ("Colesterol total", "mg/dL"),
    "LDL": ("LDL", "mg/dL"),
    "HDL": ("HDL", "mg/dL"),
    "TRIGLICER": ("Triglicérides", "mg/dL"),

    "TGO": ("TGO (AST)", "U/L"),
    "AST": ("TGO (AST)", "U/L"),
    "TGP": ("TGP (ALT)", "U/L"),
    "ALT": ("TGP (ALT)", "U/L"),

    "TSH": ("TSH ultra-sensível", "µUI/mL"),
    "T4 LIVRE": ("T4 livre", "ng/dL"),

    "HBSAG": ("HBsAg", ""),
    "ANTI-HCV": ("Anti-HCV", "")
}

if pdf:
    resultados = []

    with pdfplumber.open(pdf) as arquivo:
        for pagina in arquivo.pages:
            texto = pagina.extract_text()
            if texto:
                linhas = texto.upper().split("\n")

                for linha in linhas:
                    for chave, (nome_saida, unidade) in EXAMES.items():
                        if chave in linha:
                            # captura números ou positivo/negativo
                            numero = re.search(r"\d+,\d+|\d+\.\d+|\d+", linha)
                            positivo_negativo = re.search(r"POSITIVO|NEGATIVO|REAGENTE|NÃO REAGENTE", linha)

                            if numero:
                                valor = numero.group()
                                resultados.append(f"{nome_saida} {valor} {unidade}".strip())

                            elif positivo_negativo:
                                resultados.append(f"{nome_saida}: {positivo_negativo.group().capitalize()}")

    if resultados:
        st.subheader("📄 Dados extraídos")
        for item in sorted(set(resultados)):
            st.code(item)
    else:
        st.warning("Nenhum exame reconhecido no PDF.")

import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Resumo automático de exames", layout="centered")

st.title("🧪 Resumo automático de exames laboratoriais")
st.write("Envie o PDF do exame para gerar um resumo em texto único.")

pdf = st.file_uploader("Enviar PDF do exame", type=["pdf"])

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
                    for chave, (nome, unidade) in EXAMES.items():
                        if chave in linha:
                            numero = re.search(r"\d+,\d+|\d+\.\d+|\d+", linha)
                            status = re.search(r"POSITIVO|NEGATIVO|REAGENTE|NÃO REAGENTE", linha)

                            if numero:
                                valor = numero.group()
                                resultados.append(f"{nome} {valor} {unidade}".strip())

                            elif status:
                                resultados.append(f"{nome} {status.group().capitalize()}")

    if resultados:
        resumo = " | ".join(sorted(set(resultados)))

        st.subheader("📄 Resumo automático")
        st.code(resumo)
    else:
        st.warning("Nenhum exame reconhecido no PDF.")

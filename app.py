import streamlit as st
import pdfplumber
import re
from collections import OrderedDict

st.set_page_config(page_title="Resumo clínico automático", layout="centered")

st.title("🧪 Resumo clínico automático de exames")
st.write("Envie o PDF do exame para gerar um resumo clínico padronizado.")

pdf = st.file_uploader("Enviar PDF do exame", type=["pdf"])

# Ordem clínica padrão
ORDEM_CLINICA = [
    "Hb", "Ht", "Leu", "Plq",
    "Glicose",
    "Creatinina",
    "Colesterol total", "LDL", "HDL", "Triglicérides",
    "TGO (AST)", "TGP (ALT)",
    "Ferritina", "Vitamina B12", "Ácido fólico", "Vitamina D",
    "TSH ultra-sensível", "T4 livre",
    "HBsAg", "Anti-HCV"
]

# Dicionário de reconhecimento
EXAMES = {
    "HEMOGLOBINA": "Hb",
    "HEMATÓCRITO": "Ht",
    "LEUCÓCITOS": "Leu",
    "PLAQUETAS": "Plq",

    "GLICOSE": "Glicose",
    "CREATININA": "Creatinina",

    "COLESTEROL TOTAL": "Colesterol total",
    "LDL": "LDL",
    "HDL": "HDL",
    "TRIGLICER": "Triglicérides",

    "TGO": "TGO (AST)",
    "AST": "TGO (AST)",
    "TGP": "TGP (ALT)",
    "ALT": "TGP (ALT)",

    "FERRITINA": "Ferritina",
    "VITAMINA B12": "Vitamina B12",
    "ÁCIDO FÓLICO": "Ácido fólico",
    "VITAMINA D": "Vitamina D",

    "TSH": "TSH ultra-sensível",
    "T4 LIVRE": "T4 livre",

    "HBSAG": "HBsAg",
    "ANTI-HCV": "Anti-HCV"
}

# Regex para valor + unidade
PADRAO_VALOR_UNIDADE = re.compile(
    r"(\d+[.,]?\d*)\s*(g/dL|mg/dL|pg/mL|ng/mL|µUI/mL|UI/L|U/L|%|mm³)?",
    re.IGNORECASE
)

STATUS_REGEX = re.compile(r"POSITIVO|NEGATIVO|REAGENTE|NÃO REAGENTE", re.IGNORECASE)

if pdf:
    encontrados = {}

    with pdfplumber.open(pdf) as arquivo:
        for pagina in arquivo.pages:
            texto = pagina.extract_text()
            if not texto:
                continue

            linhas = texto.upper().split("\n")

            for linha in linhas:
                for chave, nome_padrao in EXAMES.items():
                    if chave in linha and nome_padrao not in encontrados:

                        status = STATUS_REGEX.search(linha)
                        valor_unidade = PADRAO_VALOR_UNIDADE.search(linha)

                        if status:
                            encontrados[nome_padrao] = status.group().capitalize()

                        elif valor_unidade:
                            valor = valor_unidade.group(1).replace(",", ".")
                            unidade = valor_unidade.group(2) or ""
                            encontrados[nome_padrao] = f"{valor} {unidade}".strip()

    if encontrados:
        resumo_ordenado = []

        for exame in ORDEM_CLINICA:
            if exame in encontrados:
                resumo_ordenado.append(f"{exame} {encontrados[exame]}")

        resumo_final = " | ".join(resumo_ordenado)

        st.subheader("📄 Resumo clínico")
        st.code(resumo_final)

    else:
        st.warning("Nenhum exame reconhecido no PDF.")

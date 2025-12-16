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
    "Hb", "Ht", "VCM", "HCM", "RDW", "Leu", "Plq",
    "Glicose",
    "Creatinina",
    "Colesterol total", "LDL", "HDL", "Triglicérides",
    "TGO (AST)", "TGP (ALT)",
    "Ferritina", "Vitamina B12", "Ácido fólico", "Vitamina D",
    "TSH ultra-sensível", "T4 livre",
    "HBsAg", "Anti-HCV"
]

# Reconhecimento (sinônimos reais de laudo)
EXAMES = {
    "HEMOGLOBINA": "Hb",
    "HEMATÓCRITO": "Ht",
    "VCM": "VCM",
    "HCM": "HCM",
    "RDW": "RDW",
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
    "VITAMINA B-12": "Vitamina B12",
    "VITAMINA B12": "Vitamina B12",
    "ÁCIDO FÓLICO": "Ácido fólico",
    "VITAMINA D": "Vitamina D",

    "TSH": "TSH ultra-sensível",
    "T4 LIVRE": "T4 livre",

    "HBSAG": "HBsAg",
    "ANTI-HCV": "Anti-HCV"
}

STATUS_REGEX = re.compile(r"POSITIVO|NEGATIVO|REAGENTE|NÃO REAGENTE", re.IGNORECASE)

def extrair_resultado(linha, exame):
    """
    Extrai o valor correto ignorando % quando necessário
    e priorizando o número após o nome do exame
    """
    # Remove valores de referência
    linha = re.sub(r"\(.*?\)", "", linha)
    linha = linha.replace(",", ".")

    numeros = re.findall(r"\d+\.\d+|\d+", linha)

    if not numeros:
        return None

    # Leucócitos → pega número grande (contagem)
    if exame == "Leu":
        for n in numeros:
            if float(n) > 1000:
                return n + " /mm³"

    # Plaquetas
    if exame == "Plq":
        return numeros[0] + " /mm³"

    # Percentuais
    if exame in ["Ht", "RDW"]:
        return numeros[0] + " %"

    return numeros[0]

if pdf:
    encontrados = {}

    with pdfplumber.open(pdf) as arquivo:
        for pagina in arquivo.pages:
            texto = pagina.extract_text()
            if not texto:
                continue

            linhas = texto.upper().split("\n")

            for linha in linhas:
                for chave, nome in EXAMES.items():
                    if chave in linha and nome not in encontrados:

                        status = STATUS_REGEX.search(linha)
                        if status:
                            encontrados[nome] = status.group().capitalize()
                            continue

                        valor = extrair_resultado(linha, nome)
                        if valor:
                            encontrados[nome] = valor

    if encontrados:
        resumo = []
        for exame in ORDEM_CLINICA:
            if exame in encontrados:
                resumo.append(f"{exame} {encontrados[exame]}")

        st.subheader("📄 Resumo clínico")
        st.code(" | ".join(resumo))
    else:
        st.warning("Nenhum exame reconhecido no PDF.")

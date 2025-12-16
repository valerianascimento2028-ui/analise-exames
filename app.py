import streamlit as st
import pdfplumber
import re

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

# Reconhecimento de exames
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
    linha = re.sub(r"\(.*?\)", "", linha)
    linha = linha.replace(",", ".")
    numeros = re.findall(r"\d+\.\d+|\d+", linha)

    if not numeros:
        return None

    if exame == "Leu":
        for n in numeros:
            if float(n) > 1000:
                return n + " /mm³"

    if exame == "Plq":
        return numeros[0] + " /mm³"

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
        resumo_lista = []
        for exame in ORDEM_CLINICA:
            if exame in encontrados:
                resumo_lista.append(f"{exame} {encontrados[exame]}")

        resumo_final = " | ".join(resumo_lista)

        st.subheader("📄 Resumo clínico")

        # Caixa de texto para copiar
        st.text_area(
            "👉 Copie o resumo abaixo (Ctrl + A → Ctrl + C):",
            resumo_final,
            height=150
        )

        # Botão de download
        st.download_button(
            label="📥 Baixar resumo (.txt)",
            data=resumo_final,
            file_name="resumo_exames.txt",
            mime="text/plain"
        )

    else:
        st.warning("Nenhum exame reconhecido no PDF.")

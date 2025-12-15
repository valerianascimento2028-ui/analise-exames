import pdfplumber
import re
import os

def extrair_dados_pdf_para_texto_formatado(caminho_pdf):
    """
    Extrai texto de um PDF e o formata no padrão desejado (dados separados por '|').

    Args:
        caminho_pdf (str): O caminho completo para o arquivo PDF.

    Returns:
        str or None: O texto extraído e formatado ou None em caso de erro.
    """
    dados_totais = ""
    
    try:
        # 1. Abre o PDF com pdfplumber
        with pdfplumber.open(caminho_pdf) as pdf:
            print(f"✅ PDF '{os.path.basename(caminho_pdf)}' aberto com sucesso.")
            
            # 2. Itera por cada página do PDF
            for pagina in pdf.pages:
                # Extrai o texto da página
                texto_pagina = pagina.extract_text()
                
                if texto_pagina:
                    dados_totais += texto_pagina + "\n"
        
        # 3. Limpeza e Formatação do Texto
        
        # Remover múltiplas quebras de linha e espaços desnecessários
        # Substitui quebras de linha/retorno de carro por um espaço
        texto_limpo = dados_totais.replace('\n', ' ').replace('\r', ' ')
        
        # Substitui múltiplos espaços por um único espaço
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
        
        # 4. Formatação Final: Substitui espaços por '|'
        # Nota: Esta etapa é simplificada. Para extrações precisas de exames
        # com cabeçalhos e valores, seria necessário uma lógica de parsing mais avançada.
        texto_formatado = texto_limpo.replace(' ', '|')
        
        return texto_formatado
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo não encontrado no caminho: {caminho_pdf}")
        return None
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a extração do PDF: {e}")
        return None

# --- Exemplo de Uso ---
if __name__ == "__main__":
    
    # 1. Solicita o caminho do arquivo ao usuário
    # Altere o caminho abaixo para o local do seu arquivo de teste
    caminho_arquivo = input("Por favor, digite o caminho completo do arquivo PDF do exame: ").strip()

    if not caminho_arquivo:
        print("Caminho do arquivo não pode ser vazio. Saindo.")
    else:
        # 2. Chama a função de extração
        resultado = extrair_dados_pdf_para_texto_formatado(caminho_arquivo)
        
        # 3. Exibe o resultado
        if resultado:
            print("\n--- Resultado Formatado (Dados Separados por '|') ---")
            print(resultado)
            
            # Opcional: Salvar o resultado em um arquivo de texto
            nome_saida = os.path.splitext(caminho_arquivo)[0] + "_extraido.txt"
            try:
                with open(nome_saida, 'w', encoding='utf-8') as f:
                    f.write(resultado)
                print(f"\n✨ Dados salvos com sucesso no arquivo: {nome_saida}")
            except Exception as e:
                print(f"❌ Erro ao salvar o arquivo de saída: {e}")

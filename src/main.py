import os
from ingestion import extrair_e_limpar_pdf
from preprocessing import pre_processar_sentencas
from graph_model import vetorizar_e_calcular_similaridade, calcular_textrank
from summarizer import gerar_resumo_extrativo

def main():
    # Caminhos de entrada e saída
    caminho_pdf = 'data/pdf/artigoDrogasImpactosNaCavidadeOral_ESSE1.pdf' 
    caminho_saida = 'data/processed/resumo.txt'
    
    if not os.path.exists(caminho_pdf):
        print(f"Erro: Arquivo '{caminho_pdf}' não encontrado. Verifique o caminho.")
        return

    print("Etapa 1: Ingestão e extração de dados...")
    sentencas_originais = extrair_e_limpar_pdf(caminho_pdf)
    print(f"{len(sentencas_originais)} sentenças extraídas.")

    print("Etapa 2: Pré-processamento de PLN...")
    sentencas_limpas = pre_processar_sentencas(sentencas_originais)

    print("Etapa 3: Construção da Matriz de Adjacência do Grafo (SciPy)...")
    matriz_adjacencia = vetorizar_e_calcular_similaridade(sentencas_limpas)

    print("Etapa 4: Ranqueamento e Centralidade (TextRank)...")
    scores = calcular_textrank(matriz_adjacencia)

    print("Etapa 5: Seleção e geração do resumo...")
    # Ajuste a taxa_compressao conforme a necessidade
    resumo = gerar_resumo_extrativo(sentencas_originais, scores, taxa_compressao=0.3)

    print("Etapa 6: Salvando resultado...")
    
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(resumo)


if __name__ == "__main__":
    main()
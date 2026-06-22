import os
import sys
from ingestion import extrair_e_limpar_pdf
from preprocessing import pre_processar_sentencas

from graph_model import construir_grafo, calcular_textrank
from summarizer import gerar_resumo_extrativo

def main(args):
    if len(args) < 3:
        print("Erro. Use assim: python src/main.py <caminho_pdf> <caminho_saida>")
        return

    caminho_pdf = args[1]
    caminho_saida = args[2]
    
    if not os.path.exists(caminho_pdf):
        print(f"Erro: Ficheiro '{caminho_pdf}' não encontrado. Verifique o caminho.")
        return

    print("Etapa 1: Ingestão e extração de dados...")
    sentencas_originais = extrair_e_limpar_pdf(caminho_pdf)
    print(f"{len(sentencas_originais)} sentenças extraídas.")

    print("Etapa 2: Pré-processamento...")
    sentencas_limpas = pre_processar_sentencas(sentencas_originais)

    print("Etapa 3: Construção do Grafo (Python Puro / Lista de Adjacência)...")
    grafo = construir_grafo(sentencas_limpas)

    print("Etapa 4: Ranqueamento e Centralidade...")
    scores = calcular_textrank(grafo)

    print("Etapa 5: Seleção e geração do resumo...")
    resumo = gerar_resumo_extrativo(sentencas_originais, scores, taxa_compressao=0.3, formato="paragrafos")

    print("Etapa 6: A guardar o resultado no ficheiro...")
    
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(resumo)


if __name__ == "__main__":
    main(sys.argv)
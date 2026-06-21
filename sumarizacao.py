import re
import json
import os
from pathlib import Path
from collections import deque
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PASTA_PROJETO = Path(__file__).parent
ARQUIVO_ENTRADA = PASTA_PROJETO / "docs" / "article.txt"

PASTA_RESULTADOS = PASTA_PROJETO / "resultados"
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

ARQUIVO_RESUMO = os.path.join(PASTA_RESULTADOS, "resumo_final.txt")
ARQUIVO_FRASES = os.path.join(PASTA_RESULTADOS, "frases_selecionadas.txt")
ARQUIVO_METRICAS = os.path.join(PASTA_RESULTADOS, "metricas.json")
ARQUIVO_GRAFO = os.path.join(PASTA_RESULTADOS, "grafo.json")

threshold_grafo = 0.05
limiar_redundancia = 0.70
percentual_resumo = 0.20


def carregar_texto(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def limpar_texto(texto):
    texto = re.sub(r"\s+", " ", texto)
    texto = re.sub(r"RFO UPF, Passo Fundo, v\. 29, n\.1, 2024\s*\d*", "", texto)
    return texto.strip()


def separar_frases(texto):
    frases = re.split(r"(?<=[.!?])\s+", texto)
    return [frase.strip() for frase in frases if len(frase.strip()) >= 80]


def construir_grafo(frases, threshold):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(frases)

    similaridade = cosine_similarity(tfidf_matrix)
    grafo = {i: [] for i in range(len(frases))}

    for i in range(len(frases)):
        for j in range(i + 1, len(frases)):
            peso = similaridade[i][j]

            if peso >= threshold:
                grafo[i].append((j, float(peso)))
                grafo[j].append((i, float(peso)))

    return grafo, similaridade


def pagerank(grafo, iteracoes=100, d=0.85):
    n = len(grafo)
    scores = {v: 1 / n for v in grafo}

    for _ in range(iteracoes):
        novos_scores = {}

        for v in grafo:
            soma = 0

            for u in grafo:
                soma_pesos_u = sum(peso for _, peso in grafo[u])

                if soma_pesos_u == 0:
                    continue

                for vizinho, peso in grafo[u]:
                    if vizinho == v:
                        soma += (peso / soma_pesos_u) * scores[u]
                        break

            novos_scores[v] = (1 - d) / n + d * soma

        scores = novos_scores

    return scores


def selecionar_sem_redundancia_com_limite(
    frases_ranqueadas,
    frases,
    similaridade,
    limiar_redundancia,
    limite_palavras_resumo
):
    selecionadas = []
    palavras_resumo = 0

    for indice, score in frases_ranqueadas:
        frase = frases[indice]
        qtd_palavras_frase = len(frase.split())

        redundante = False

        for indice_escolhido, _ in selecionadas:
            if similaridade[indice][indice_escolhido] >= limiar_redundancia:
                redundante = True
                break

        if not redundante and palavras_resumo + qtd_palavras_frase <= limite_palavras_resumo:
            selecionadas.append((indice, score))
            palavras_resumo += qtd_palavras_frase

    return selecionadas, palavras_resumo


def salvar_resumo(caminho, resumo):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(resumo)


def salvar_frases_selecionadas(caminho, selecionadas, frases):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for indice, score in selecionadas:
            arquivo.write(f"F{indice + 1} | PageRank: {round(score, 5)}\n")
            arquivo.write(frases[indice] + "\n\n")


def salvar_metricas(caminho, metricas):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(metricas, arquivo, ensure_ascii=False, indent=4)


def salvar_grafo(caminho, grafo):
    grafo_serializado = {}

    for vertice, vizinhos in grafo.items():
        grafo_serializado[f"F{vertice + 1}"] = [
            {
                "vizinho": f"F{vizinho + 1}",
                "peso": round(peso, 5)
            }
            for vizinho, peso in vizinhos
        ]

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(grafo_serializado, arquivo, ensure_ascii=False, indent=4)


texto = carregar_texto(ARQUIVO_ENTRADA)
texto = limpar_texto(texto)
frases = separar_frases(texto)

grafo, similaridade = construir_grafo(frases, threshold_grafo)
scores = pagerank(grafo)

frases_ranqueadas = sorted(
    scores.items(),
    key=lambda item: item[1],
    reverse=True
)

total_palavras_texto = len(" ".join(frases).split())
limite_palavras_resumo = int(total_palavras_texto * percentual_resumo)

selecionadas, palavras_resumo = selecionar_sem_redundancia_com_limite(
    frases_ranqueadas,
    frases,
    similaridade,
    limiar_redundancia,
    limite_palavras_resumo
)

indices_ordenados = sorted([indice for indice, _ in selecionadas])

fila_resumo = deque(indices_ordenados)
resumo = []

while fila_resumo:
    indice = fila_resumo.popleft()
    resumo.append(frases[indice])

resumo_final = " ".join(resumo)

total_vertices = len(grafo)
total_arestas = sum(len(vizinhos) for vizinhos in grafo.values()) // 2

densidade = 0
if total_vertices > 1:
    densidade = (2 * total_arestas) / (total_vertices * (total_vertices - 1))

taxa_compressao_real = 0
if total_palavras_texto > 0:
    taxa_compressao_real = palavras_resumo / total_palavras_texto

metricas = {
    "total_frases_extraidas": len(frases),
    "total_vertices": total_vertices,
    "total_arestas": total_arestas,
    "densidade_grafo": round(densidade, 5),
    "threshold_grafo": threshold_grafo,
    "limiar_redundancia": limiar_redundancia,
    "percentual_resumo_configurado": percentual_resumo,
    "total_palavras_texto": total_palavras_texto,
    "limite_palavras_resumo": limite_palavras_resumo,
    "total_palavras_resumo": palavras_resumo,
    "taxa_compressao_real": round(taxa_compressao_real, 5),
    "quantidade_frases_selecionadas": len(selecionadas)
}

salvar_resumo(ARQUIVO_RESUMO, resumo_final)
salvar_frases_selecionadas(ARQUIVO_FRASES, selecionadas, frases)
salvar_metricas(ARQUIVO_METRICAS, metricas)
salvar_grafo(ARQUIVO_GRAFO, grafo)

print("Arquivos gerados na pasta 'resultados'.")

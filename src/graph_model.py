import numpy as np
from scipy.spatial.distance import pdist, squareform

def vetorizar_e_calcular_similaridade(sentencas_limpas):
    vocabulario = set()
    for sentenca in sentencas_limpas:
        vocabulario.update(sentenca.split())
    
    vocabulario = list(vocabulario)
    word_to_index = {word: i for i, word in enumerate(vocabulario)}
    
    num_sentencas = len(sentencas_limpas)
    matriz_frequencia = np.zeros((num_sentencas, len(vocabulario)))
    
    for i, sentenca in enumerate(sentencas_limpas):
        for palavra in sentenca.split():
            if palavra in word_to_index:
                matriz_frequencia[i, word_to_index[palavra]] += 1
                
    if matriz_frequencia.any():
        distancias_cosseno = pdist(matriz_frequencia, metric='cosine')
        matriz_distancia = squareform(distancias_cosseno)
        matriz_similaridade = 1 - matriz_distancia
    else:
        matriz_similaridade = np.zeros((num_sentencas, num_sentencas))
        
    np.fill_diagonal(matriz_similaridade, 0)
    
    return matriz_similaridade

def calcular_textrank(matriz_similaridade, d=0.85, iteracoes=100, erro_min=1e-4):
    num_nos = matriz_similaridade.shape[0]
    scores = np.ones(num_nos)
    
    # Normalização da matriz de transição
    somas = matriz_similaridade.sum(axis=1)
    matriz_transicao = np.zeros_like(matriz_similaridade)
    for i in range(num_nos):
        if somas[i] != 0:
            matriz_transicao[i] = matriz_similaridade[i] / somas[i]
            
    # Execução iterativa do algoritmo de centralidade
    for _ in range(iteracoes):
        novos_scores = (1 - d) + d * np.dot(matriz_transicao.T, scores)
        if np.linalg.norm(novos_scores - scores) < erro_min:
            break
        scores = novos_scores
        
    return scores
import math

def calcular_similaridade_cosseno(vetor1, vetor2):
    """Calcula o cosseno do ângulo entre dois vetores"""
    produto_escalar = sum(a * b for a, b in zip(vetor1, vetor2))
    norma1 = math.sqrt(sum(a * a for a in vetor1))
    norma2 = math.sqrt(sum(b * b for b in vetor2))
    
    if norma1 == 0 or norma2 == 0:
        return 0.0
    return produto_escalar / (norma1 * norma2)

def construir_grafo(sentencas_limpas, limiar=0.1):
    """
    Constrói a representação estrutural do grafo (Lista de Adjacência).
    Vértices: Índices das frases.
    Arestas: Dicionário de conexões com pesos de similaridade.
    """
    vocabulario = list(set(palavra for sentenca in sentencas_limpas for palavra in sentenca.split()))
    word_to_index = {word: i for i, word in enumerate(vocabulario)}
    
    vetores = []
    for sentenca in sentencas_limpas:
        vetor = [0] * len(vocabulario)
        for palavra in sentenca.split():
            if palavra in word_to_index:
                vetor[word_to_index[palavra]] += 1
        vetores.append(vetor)
    
    num_sentencas = len(sentencas_limpas)
    grafo = {i: {} for i in range(num_sentencas)}
    
    for i in range(num_sentencas):
        for j in range(i + 1, num_sentencas):
            sim = calcular_similaridade_cosseno(vetores[i], vetores[j])
            # Aplica o limiar (threshold) para isolar redundâncias fracas
            if sim >= limiar:
                grafo[i][j] = sim
                grafo[j][i] = sim
                
    return grafo

def calcular_textrank(grafo, d=0.85, iteracoes=50, erro_min=1e-4):
    """
    Algoritmo de centralidade TextRank.
    Calcula recursivamente a importância de cada vértice na rede.
    """
    num_nos = len(grafo)
    if num_nos == 0:
        return {}
    scores = {i: 1.0 for i in range(num_nos)}

    pesos_saida = {no: sum(grafo[no].values()) for no in grafo}
    
    for _ in range(iteracoes):
        novos_scores = {}
        convergencia = True
        
        for no_i in grafo:
            soma_votos = 0.0
            for no_j in grafo:
                if no_i in grafo[no_j] and pesos_saida[no_j] > 0:
                    soma_votos += (scores[no_j] * grafo[no_j][no_i]) / pesos_saida[no_j]
            
            novos_scores[no_i] = (1 - d) + d * soma_votos
            if abs(novos_scores[no_i] - scores[no_i]) > erro_min:
                convergencia = False
                
        scores = novos_scores
        if convergencia:
            break
            
    return scores
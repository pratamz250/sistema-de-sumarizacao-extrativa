class MaxHeap:
    """
    Garante a organização de prioridade das frases mais relevantes.
    """
    def __init__(self):
        self.heap = []

    def inserir(self, item):
        self.heap.append(item)
        self._subir(len(self.heap) - 1)

    def extrair_maximo(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        maximo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._descer(0)
        return maximo

    def _subir(self, index):
        pai = (index - 1) // 2
        if index > 0 and self.heap[index][0] > self.heap[pai][0]:
            self.heap[index], self.heap[pai] = self.heap[pai], self.heap[index]
            self._subir(pai)

    def _descer(self, index):
        maior = index
        esquerdo = 2 * index + 1
        direito = 2 * index + 2
        
        if esquerdo < len(self.heap) and self.heap[esquerdo][0] > self.heap[maior][0]:
            maior = esquerdo
        if direito < len(self.heap) and self.heap[direito][0] > self.heap[maior][0]:
            maior = direito
            
        if maior != index:
            self.heap[index], self.heap[maior] = self.heap[maior], self.heap[index]
            self._descer(maior)


def gerar_resumo_extrativo(sentencas_originais, scores, taxa_compressao=0.3, formato="paragrafos"):
    qtd_frases = max(1, int(len(sentencas_originais) * taxa_compressao))
    
    fila_prioridade = MaxHeap()
    
    for i in range(len(sentencas_originais)):
        fila_prioridade.inserir((scores[i], i, sentencas_originais[i]))
        
    top_frases = []
    for _ in range(qtd_frases):
        item = fila_prioridade.extrair_maximo()
        if item:
            top_frases.append(item)
            
    top_frases_cronologicas = sorted(top_frases, key=lambda x: x[1])
    
    if formato == "topicos":
        resumo_final = "\n".join([f"• {frase[2]}" for frase in top_frases_cronologicas])
    else:
        resumo_final = "\n\n".join([frase[2] for frase in top_frases_cronologicas])
        
    return resumo_final
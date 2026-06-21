# Sistema de Sumarizacao Extrativa

Este projeto gera um resumo extrativo a partir de um texto de entrada. O resumo e formado por frases do proprio artigo, escolhidas de acordo com a relevancia calculada por similaridade textual e PageRank.

## Fluxo do algoritmo

**Carrega o texto:** carrega o conteudo do arquivo `docs/article.txt`.

**Limpeza:** remove espacos repetidos e trechos indesejados do texto, deixando o conteudo mais uniforme para processamento.

**Separa frases:** separa o texto em frases e descarta frases muito curtas, que normalmente carregam pouca informacao para o resumo.

**TF-IDF:** transforma cada frase em um vetor numerico, destacando palavras importantes em cada frase em relacao ao conjunto completo.

**Similaridade do cosseno:** compara os vetores das frases para medir o quanto elas sao parecidas entre si. "O quanto duas frases são parecidas?"

**Grafo ponderado:** cria um grafo em que cada frase e um vertice, e as arestas representam similaridades acima do limiar definido.

**PageRank:** calcula a importancia de cada frase com base nas conexoes do grafo. Frases parecidas com muitas frases relevantes tendem a receber pontuacao maior. "Qual frase é mais importante dentro do grafo?"

**Remocao de redundancia:** evita selecionar frases muito parecidas entre si, reduzindo repeticoes no resumo.

**Limite de 20%:** limita o tamanho do resumo a aproximadamente 20% da quantidade de palavras do texto original processado.

**Fila:** ordena as frases selecionadas pela posicao original no texto, preservando a ordem natural da leitura.

**Resumo final:** junta as frases selecionadas e salva o resultado em `resultados/resumo_final.txt`.

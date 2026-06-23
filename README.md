# Sistema de Sumarização Extrativa Baseado em Grafos

Este projeto gera um resumo extrativo automático a partir de um documento de entrada (PDF ou TXT). O resumo é formado por frases do próprio texto original, escolhidas de acordo com sua relevância estrutural e semântica, calculada através de similaridade textual e algoritmos de centralidade em grafos (TextRank/PageRank).

## Fluxo do Algoritmo

O pipeline de dados da aplicação segue as seguintes etapas:

1. **Extração do PDF:** Abre o arquivo PDF, percorre todas as páginas e reúne o texto extraído em um único conteúdo.
2. **Delimitação do conteúdo:** Localiza as frases inicial e final informadas na execução e mantém somente o trecho compreendido entre elas.
3. **Limpeza do texto:** Remove indicações de página, hifenizações causadas por quebras de linha, quebras de linha e espaços repetidos.
4. **Separação das frases:** Segmenta o texto em sentenças com o NLTK e descarta aquelas que possuem três palavras ou menos.
5. **Pré-processamento:** Converte as frases para minúsculas, remove pontuação e stopwords da língua portuguesa e reduz as palavras aos seus radicais com stemming.
6. **Vetorização por frequência:** Cria um vocabulário com as palavras processadas e representa cada frase por um vetor contendo a frequência de cada palavra.
7. **Similaridade do cosseno:** Calcula a similaridade entre os vetores de cada par de frases.
8. **Construção do grafo ponderado:** Representa cada frase como um vértice e conecta frases com similaridade igual ou superior a `0.1`, utilizando a similaridade como peso da aresta.
9. **Ranqueamento TextRank:** Calcula a pontuação de importância de cada frase a partir das conexões e dos pesos do grafo.
10. **Seleção e ordenação:** Utiliza uma fila de prioridade máxima para selecionar aproximadamente 30% das frases com maiores pontuações e depois as reorganiza conforme a ordem em que aparecem no documento.
11. **Geração do resumo:** Junta as frases selecionadas em parágrafos ou tópicos e grava o resultado em um arquivo de texto no caminho de saída informado.

---

## Estrutura do Projeto

Recomenda-se organizar os arquivos da seguinte maneira:

```text
meu_sumarizador/
│
├── data/
│   ├── raw/               # Coloque seus arquivos originais aqui (ex: pcdt.pdf)
│   └── processed/         # Onde os resumos gerados (.txt) serão salvos
│
├── src/
│   ├── ingestion.py       # Lógica de leitura de arquivos e Regex
│   ├── preprocessing.py   # Limpeza de linguagem natural (PLN)
│   ├── graph_model.py     # Criação da matriz, Grafo e PageRank
│   └── summarizer.py      # Seleção, ordenação e formatação do texto
│
├── main.py                # Script principal que orquestra a aplicação
├── requirements.txt       # Lista de dependências do Python
└── README.md              # Este arquivo de documentação

```

---

## ⚙️ Pré-requisitos e Instalação

Para rodar a aplicação, você precisará do **Python 3.8** (ou superior) instalado em sua máquina.

**1. Clone ou baixe este repositório.**
Abra o terminal e navegue até a pasta raiz do projeto.

**2. Crie um ambiente virtual (Opcional, mas recomendado):**
Isso evita que as bibliotecas do projeto entrem em conflito com outras instaladas no seu computador.

* **No Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **No Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate

```



**3. Instale as dependências:**
Certifique-se de que o arquivo `requirements.txt` contém as bibliotecas: `pdfplumber`, `nltk`, `scipy` e `numpy`. Para instalar todas de uma vez, execute:

```bash
pip install -r requirements.txt

```

**4. Baixar o NLTK:**
É preciso fazer o setup do NLTK para rodar o projeto. Execute:
```bash
python src/setup_nltk.py
```

*(Nota: Assim o NLTK é baixado apenas uma vez e o script verifica se já foi baixado em outras execuções).*

---

## Como Executar o Projeto

1. **Adicione o arquivo de entrada:**
Coloque o arquivo que você deseja resumir (PDF ou TXT) na pasta correspondente. Por padrão, o script busca em `data/raw/` ou `data/pdf/`.


2. **Execute o script principal:**
No terminal, na raiz do projeto, digite:
```bash
python src/main.py <caminho_pdf> <caminho_saida> "<frase inicial>" "<frase final>"

```

*(Nota: as entradas "\<frase inicial\>" e "\<frase final\>" correspondem aos escopos inicial e final, respectivamente, de onde o resumo vai começar 
terminar. Por exemplo, se quiser ignorar a seção "agradecimentos" do seu artigo e também a seção "referências").*


3. **Verifique o resultado:**
O terminal exibirá o progresso de cada etapa (Ingestão, Pré-processamento, Grafo, etc). Ao finalizar com sucesso, o seu resumo estruturado estará salvo e pronto para leitura no caminho de saída definido (ex: `data/processed/resumo_final.txt`).

## Exemplo de uso

1. **Exemplo após instalação de depêndias e setup:**
```bash
python src/main.py data/pdf/artigo1.pdf data/processed/resumo_artigo1.txt "Discussão" "Referências"
```

## Executar os PDFs incluídos no projeto

Execute os comandos abaixo a partir da pasta raiz do projeto. Cada artigo gera um arquivo de saída diferente em `data/processed/`, evitando que um resumo substitua o anterior.

As duas frases no final de cada comando delimitam o conteúdo processado: a primeira marca o início do trecho e a segunda marca onde a extração deve terminar.

### 1. Drogas e seus impactos na cavidade oral

Processa o conteúdo entre as seções **Revisão de literatura** e **Considerações finais**:

```bash
python src/main.py data/pdf/artigoDrogasImpactosNaCavidadeOral_ESSE1.pdf data/processed/resumo_drogas_cavidade_oral.txt "Revisão de literatura" "Considerações finais"
```

### 2. Epidemiologia e prevenção do traumatismo dentário

Processa o conteúdo entre as seções **Introdução** e **Considerações finais**:

```bash
python src/main.py data/pdf/epidemiologiaFatoresEtiologicosMeiosPrevencaoAssiciadosAoTraumatismoDentario_ESSE2.pdf data/processed/resumo_traumatismo_dentario.txt "INTRODUÇÃO" "CONSIDERAÇÕES FINAIS"
```

### 3. Causas e tratamento da periodontite

Processa o conteúdo entre as seções **Tipos de periodontite e suas características** e **Metodologia**:

```bash
python src/main.py data/pdf/causasETratamentoDePeriondontite_ESSE3.pdf data/processed/resumo_periodontite.txt "TIPOS DE PERIODONTITE E SUAS CARACTERÍSTICAS" "METODOLOGIA"
```

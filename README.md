# Sistema de Sumarização Extrativa Baseado em Grafos

Este projeto gera um resumo extrativo automático a partir de um documento de entrada (PDF ou TXT). O resumo é formado por frases do próprio texto original, escolhidas de acordo com sua relevância estrutural e semântica, calculada através de similaridade textual e algoritmos de centralidade em grafos (TextRank/PageRank).

## Fluxo do Algoritmo

O pipeline de dados da aplicação segue as seguintes etapas:

1. **Carrega o texto:** Ingestão do conteúdo bruto do arquivo de origem (ex: `data/raw/documento.pdf` ou `docs/article.txt`).
2. **Limpeza:** Remove espaços repetidos, quebras de linha indesejadas, paginações e trechos irrelevantes, deixando o conteúdo mais uniforme para processamento.
3. **Separa frases:** Segmenta o texto em sentenças individuais e descarta frases muito curtas, que normalmente carregam pouca informação útil para o resumo.
4. **Vetorização (TF-IDF / Frequência):** Transforma cada frase em um vetor numérico, destacando palavras importantes em cada frase em relação ao conjunto completo e removendo ruídos (stopwords).
5. **Similaridade do cosseno:** Compara os vetores das frases para medir o quanto elas são parecidas entre si. Responde à pergunta: *"O quanto duas frases abordam o mesmo contexto?"*
6. **Grafo ponderado:** Cria uma rede (grafo) em que cada frase é um vértice (nó), e as arestas representam as similaridades que ficaram acima do limiar definido.
7. **PageRank (TextRank):** Calcula a importância de cada frase com base nas conexões do grafo. Frases parecidas com muitas outras frases relevantes tendem a receber uma pontuação maior. Responde à pergunta: *"Qual frase é a mais central e importante dentro do documento?"*
8. **Remoção de redundância:** Aplica filtros para evitar a seleção de frases muito parecidas entre si, reduzindo repetições no texto final.
9. **Limite de compressão (20%):** Limita o tamanho do resumo a uma porcentagem específica (ex: 20% ou 30%) da quantidade de frases do texto original processado.
10. **Ordenação (Fila/Lista):** Ordena as frases selecionadas vencedoras pela sua posição original no texto-base, preservando a cronologia e a ordem natural da leitura.
11. **Resumo final:** Junta as frases selecionadas, formata em parágrafos ou tópicos e salva o resultado automaticamente na pasta de saída (ex: `data/processed/.txt`).

---

## 📂 Estrutura do Projeto

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

## 🚀 Como Executar o Projeto

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

## 🎯 Exemplo de uso

1. **Exemplo após instalação de depêndias e setup:**
```bash
python src/main.py data/pdf/artigo1.pdf data/processed/resumo_artigo1.txt "Discussão" "Referências"
```
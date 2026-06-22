import nltk

def ensure(resource, path):
    try:
        nltk.data.find(path)
        print(f"{resource} já instalado.")
    except LookupError:
        print(f"Baixando {resource}...")
        nltk.download(resource)

def main():
    ensure("punkt", "tokenizers/punkt")
    ensure("stopwords", "corpora/stopwords")

    ensure("punkt_tab", "tokenizers/punkt_tab")

    print("NLTK pronto.")

if __name__ == "__main__":
    main()
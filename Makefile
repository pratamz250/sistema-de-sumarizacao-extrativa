VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

nltk-data:
	$(PYTHON) -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

spacy-model:
	$(PYTHON) -m spacy download pt_core_news_sm

setup: install nltk-data spacy-model

run:
	$(PYTHON) src/main.py

clean:
	rm -rf $(VENV)

.PHONY: venv install nltk-data spacy-model setup run clean
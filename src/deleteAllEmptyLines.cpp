#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char *argv[]) {
	if(argc != 3){
		cout << "Error. Run: $ deleteAllEmptyLines.x <entrada> <saida>" << endl;
		exit(1);
	}

	string entrada = argv[1];
	string saida = argv[2];

	ifstream in(entrada);
	ofstream out(saida);

	if (!in.is_open()) {
		cerr << "Erro ao abrir o arquivo de entrada.\n";
		return 1;
	}

	if (!out.is_open()) {
		cerr << "Erro ao criar o arquivo de saída.\n";
		return 1;
	}

	string linha;
	while (getline(in, linha)) {
		size_t inicio = linha.find_first_not_of(" \t\r");
		size_t fim = linha.find_last_not_of(" \t\r");

		if (inicio != string::npos && fim != string::npos) {
			linha = linha.substr(inicio, fim - inicio + 1);
		} else {
			linha.clear();
		}

		if (!linha.empty()) {
			out << linha << '\n';
		}
	}

	cout << "Arquivo '" << saida << "' criado sem as linhas em branco.\n";

	return 0;
}


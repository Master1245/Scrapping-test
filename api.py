from flask import Flask, jsonify
import glob, json

app = Flask(__name__)

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    """
        Lê todos os arquivos JSON na pasta 'data', junta os dados e retorna uma lista consolidada,
        ordenada pela data de coleta (do mais recente para o mais antigo).
    """
    arquivos = glob.glob("data/*.json")
    produtos = []
    for arq in arquivos:
        with open(arq, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
                # Se o conteúdo for uma lista, estenda a lista de produtos
                if isinstance(dados, list):
                    produtos.extend(dados)
                else:
                    produtos.append(dados)
            except Exception as e:
                print(f"Erro ao ler {arq}: {e}")
    # Filtra somente os itens que são dicionários
    produtos_validos = [p for p in produtos if isinstance(p, dict)]
    produtos_ordenados = sorted(produtos_validos, key=lambda x: x.get("timestamp_coleta", ""), reverse=True)
    return jsonify(produtos_ordenados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

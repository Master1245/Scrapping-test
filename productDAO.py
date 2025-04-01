import json
import os
import glob
from pathlib import Path
from typing import List
from productMODEL import ProdutoModel

class ProdutoDAO:
    ARQUIVO = 'produtos.json'

    @classmethod
    def _salvar_dados(cls, novos_dados: list):
        """
            Lê dados existentes (se houver), adiciona os novos dados e sobrescreve o arquivo.
        """
        try:
            caminho_arquivo = f"data/{cls.ARQUIVO}"
            
            # Lê dados existentes se o arquivo já existir
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    try:
                        dados_existentes = json.load(f)
                        if not isinstance(dados_existentes, list):
                            dados_existentes = []
                    except json.JSONDecodeError:
                        dados_existentes = []
            else:
                dados_existentes = []

            # Adiciona os novos dados à lista existente
            dados_existentes.extend(novos_dados)

            # Salva o arquivo consolidado
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_existentes, f, ensure_ascii=False, indent=4)

            print(f"Arquivo {cls.ARQUIVO} atualizado com sucesso!")
        
        except Exception as e:
            print(f"Erro grave ao salvar dados: {str(e)}")

    @classmethod
    def salvar_todos(cls, produtos: List[ProdutoModel]):
        """
            Converte uma lista de objetos ProdutoModel em dicionários e salva.
        """
        novos_dados = [p.to_dict() for p in produtos]
        cls._salvar_dados(novos_dados)

    @classmethod
    def consolidar_dados(cls):
        """
            Lê todos os arquivos JSON na pasta 'data' (exceto o consolidado),
            junta seus conteúdos, salva no arquivo consolidado e remove os arquivos individuais.
        """
        arquivos = glob.glob("data/*.json")
        dados_consolidados = []
        
        for arq in arquivos:
            if os.path.basename(arq) == cls.ARQUIVO:
                continue
            
            try:
                with open(arq, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    if isinstance(dados, list):
                        dados_consolidados.extend(dados)
                    else:
                        dados_consolidados.append(dados)
            except Exception as e:
                print(f"Erro ao ler o arquivo {arq}: {str(e)}")

        cls._salvar_dados(dados_consolidados)

        # Remove os arquivos individuais, mantendo apenas o consolidado
        for arq in arquivos:
            if os.path.basename(arq) != cls.ARQUIVO:
                try:
                    os.remove(arq)
                    print(f"Arquivo {arq} removido após consolidação.")
                except Exception as e:
                    print(f"Erro ao remover {arq}: {str(e)}")
    
    @classmethod
    def purge_produtct_in_file(cls):
        """
            Remove o arquivo consolidado produtos.json se existir.
        """
        caminho_arquivo = Path(f"data/{cls.ARQUIVO}")
        if caminho_arquivo.exists():
            try:
                caminho_arquivo.unlink()
                print(f"Arquivo {cls.ARQUIVO} removido.")
            except Exception as e:
                print(f"Erro ao remover {cls.ARQUIVO}: {str(e)}")
        else:
            print(f"O arquivo {cls.ARQUIVO} não existe.")
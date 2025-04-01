class ProdutoModel:
    def __init__(self, nome: str, preco_avista: float, preco_prazo: float, 
                 disponibilidade: str, url: str, timestamp_coleta: str):
        self.nome = nome
        self.preco_avista = preco_avista
        self.preco_prazo = preco_prazo
        self.disponibilidade = disponibilidade
        self.url = url
        self.timestamp_coleta = timestamp_coleta

    def __repr__(self):
        return f"Produto({self.nome})"
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "preco_avista": self.preco_avista,
            "preco_prazo": self.preco_prazo,
            "disponibilidade": self.disponibilidade,
            "url": self.url,
            "timestamp_coleta": self.timestamp_coleta
        }
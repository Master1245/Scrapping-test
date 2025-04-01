from productMODEL import ProdutoModel
import datetime

class ProdutoBO:

    @staticmethod
    def criar_produto_amazon(promo_data: dict) -> ProdutoModel:
        """
            Extrai os dados relevantes de um dicionário de promoção da Amazon e retorna um objeto ProdutoModel.
        """
        product = promo_data.get('product', {}).get('entity', {})
        
        # Extração do nome
        nome = product.get('title', {}).get('entity', {}).get('displayString', 'Sem título')
    
        
        # Extração de preços
        buying_options = product.get('buyingOptions', [{}])
        primeiro_opcao = buying_options[0] if buying_options else {}
        
        # Preço à vista
        preco_avista = primeiro_opcao.get("price", {}).get("entity", {}).get("priceToPay", {}).get(
            "moneyValueOrRange", {}).get("value", {}).get("amount")
        
        # Verificação de promoções
        promotions = primeiro_opcao.get("promotionsUnified", {}).get("entity", {}).get("displayablePromotions", [])
        if promotions:
            savings = promotions[0].get("combinedSavings", {})
            if savings:
                preco_avista = savings.get("fixedTargetAmount", {}).get("amount", preco_avista)
        
        # Preço a prazo
        preco_prazo = primeiro_opcao.get("price", {}).get("entity", {}).get("priceToPay", {}).get(
            "moneyValueOrRange", {}).get("value", {}).get("amount", "N/D")
        
        # Tratamento especial para Prime
        fragments = product.get("buyingOptions", [{}])[0].get("dealBadge", {}).get(
            "entity", {}).get("messaging", {}).get("content", {}).get("fragments", [])
        
        if fragments and fragments[0].get("text") == "Com Prime":
            preco_avista = f"{preco_avista} Com Prime"
            if len(buying_options) >= 2:
                preco_prazo = buying_options[1].get("price", {}).get("entity", {}).get(
                    "priceToPay", {}).get("moneyValueOrRange", {}).get("value", {}).get("amount", "N/D")

        # Disponibilidade
        disponibilidade = "Indisponível"
        for opcao in buying_options:
            deal_state = opcao.get("dealDetails", {}).get("entity", {}).get("state")
            if deal_state:
                disponibilidade = deal_state
                break
        
        # URL do produto
        url = product.get('links', {}).get('entity', {}).get('viewOnAmazon', {}).get('url', '')
        
        timestamp_coleta = datetime.datetime.now().isoformat()

        return ProdutoModel(
            nome=nome,
            preco_avista=preco_avista,
            preco_prazo=preco_prazo,
            disponibilidade=disponibilidade,
            url="https://www.amazon.com.br/"+url,
            timestamp_coleta=timestamp_coleta
        )
 
    @staticmethod
    def criar_produto_magazine_luiza(dados_brutos: dict) -> ProdutoModel:
        """
            Extrai os dados relevantes de um dicionário retornado pelo Magazine Luiza e retorna um objeto ProdutoModel.
        """
        if dados_brutos.get('installment', {}):
            preco_prazo = dados_brutos.get('installment', {}).get('value', {}).get('amount')
        else:
            preco_prazo = dados_brutos.get('price', {}).get('bestPrice')

        return ProdutoModel(
            nome=dados_brutos.get('title', 'Sem título'),
            preco_avista=dados_brutos.get('price', {}).get('bestPrice'),
            preco_prazo=preco_prazo,
            disponibilidade='AVAILABLE' if dados_brutos.get('available') else 'UNAVAILABLE',
            url=f"https://www.magazineluiza.com.br/{dados_brutos.get('path', '')}",
            timestamp_coleta=datetime.datetime.now().isoformat()
        )
import requests
from bs4 import BeautifulSoup
import json
import re
import random
from json import JSONDecodeError
from productBO import ProdutoBO


def extract_and_parse_json(script_content):
    """
        Usa regex para extrair um objeto JSON de um conteúdo de script e o retorna como dicionário.
    """
    pattern = r'assets\.mountWidget\(\s*[\'"][^\'"]+[\'"],\s*({.*?})\s*\)\s*;'
    match = re.search(pattern, script_content, re.DOTALL)

    json_str = match.group(1)

    pattern = r'"prefetchedData"\s*:\s*(.*)'
    match = re.search(pattern, json_str, re.DOTALL)
    if match is not None:
        json_str = match.group(1)
        conteudo = re.sub(r',$', '', json_str.strip())

        if conteudo.startswith('{'):
            count = 0
            end_index = None
            for i, char in enumerate(conteudo):
                if char == '{':
                    count += 1
                elif char == '}':
                    count -= 1
                    if count == 0:
                        end_index = i + 1
                        break
            if end_index is not None:
                json_candidate = conteudo[:end_index]
            else:
                json_candidate = conteudo
        else:
            json_candidate = conteudo
        try:   
            return json.loads(json_candidate)
        except JSONDecodeError as e:
            error_pos = e.pos
            start = max(0, error_pos - 50)
            end = min(len(json_str), error_pos + 50)
            context = json_str[start:end]
            print(f"ERRO NA COLUNA {error_pos}:\n{context}")
    else:
        print("Match regex null")
        return 

def scrape_amazon(url):
    """
        Realiza requisição HTTP para a URL da Amazon, extrai dados via BeautifulSoup e 
        utiliza ProdutoBO para criar os objetos de produto.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        scripts = soup.find_all('script', string=lambda t: t and 'DiscountsWidgetsHorizonteAssets' in t)
        
        if not scripts:
            scrape_amazon(url)
            return

        data = extract_and_parse_json(scripts[0].string)

        if not data:
            scrape_amazon(url)
        
        promotions = data.get('entity', {}).get('rankedPromotions', [])

        list_product = []
        for promo in promotions:
            produto = ProdutoBO.criar_produto_amazon(promo)
            list_product.append(produto)
        return list_product
    except Exception:
            scrape_amazon(url)   

def get_random_headers():
    """
        Retorna um dicionário de headers aleatórios para simular diferentes user-agents.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.magazineluiza.com.br/',
        'DNT': str(random.randint(1, 2)),
        'Connection': 'keep-alive'
    }

def scrape_magazine_luiza(url):
    """
        Realiza o scraping no Magazine Luiza:
      - Cria sessão e faz requisições.
      - Verifica se há bloqueio.
      - Procura o script '__NEXT_DATA__' e extrai os produtos.
      - Usa ProdutoBO para criar os objetos de produto.
    """
    try:
        with requests.Session() as session:
            # Primeira requisição para estabelecer sessão
            session.get(url, headers=get_random_headers())
            
            # Requisição principal com delays aleatórios
            response = session.get(
                url,
                headers=get_random_headers(),
                timeout=10,
                allow_redirects=True
            )
            
            if "Pedimos desculpas pela inconveniência" in response.text:
                print("Bloqueio detectado! Tente estas soluções:")
                print("1. Use proxies rotativos")
                print("2. Aumente o intervalo entre requisições")
                print("3. Implemente verificação de CAPTCHA")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
            if not next_data_script:
                print("Não foi possível encontrar o script __NEXT_DATA__ na página.")
                scrape_magazine_luiza(url)
                return None
                    
            try:
                json_data = json.loads(next_data_script.string)
            except Exception as e:
                print(f"Erro ao carregar JSON: {e}")
                return None
            products = json_data['props']['pageProps']['data']['search']['products']
            list_product = []
            for produto in products:
                if not produto.get('ads'):
                    produto_obj = ProdutoBO.criar_produto_magazine_luiza(produto)
                    list_product.append(produto_obj)
            return list_product
    except Exception:
        scrape_magazine_luiza(url)
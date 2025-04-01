from celery import Celery
from celery.schedules import crontab
import json
import os
import datetime
from scraper import scrape_amazon, scrape_magazine_luiza
from productDAO import ProdutoDAO
from productMODEL import ProdutoModel

# Configuração do Celery usando Redis como broker (o Redis é configurado via Docker Compose)
app = Celery('tasks', broker='redis://redis:6379/0')

# Configuração do agendador Celery Beat para executar as tarefas a cada 1 minuto
app.conf.beat_schedule = {
    "scrape_amazon_cada_1m": {
        "task": "tasks.tarefa_scraping_amazon",
        "schedule": crontab(minute='*/1'),
        "args": ("https://www.amazon.com.br/gp/goldbox",)
    },
    "scrape_magazine_cada_1m": {
        "task": "tasks.tarefa_scraping_magazine",
        "schedule": crontab(minute='*/1'),
        "args": ("https://www.magazineluiza.com.br/busca/ofertas+do+dia/",)
    },
}


def salvar_dados(dados, marketplace):
    """
        Cria a pasta 'data' (se não existir) e salva os dados em um arquivo JSON.
        Se os dados forem objetos ProdutoModel, converte-os para dicionários.
    """
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"data/{marketplace}_{timestamp}.json"
    
    # Se dados for uma lista de objetos ProdutoModel, converte para lista de dicionários
    if isinstance(dados, list):
        dados = [produto.to_dict() if isinstance(produto, ProdutoModel) else produto for produto in dados]

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


@app.task
def tarefa_scraping_amazon(url):
    """
        Tarefa que realiza o scraping na Amazon utilizando a função scrape_amazon.
        Salva os dados obtidos e consolida os arquivos de dados.
    """
    dados = scrape_amazon(url)
    if dados:  
        salvar_dados(dados, "amazon")
        ProdutoDAO.consolidar_dados()

@app.task
def tarefa_scraping_magazine(url):
    """
        Tarefa que realiza o scraping no Magazine Luiza utilizando a função scrape_magazine_luiza.
        Salva os dados obtidos e consolida os arquivos de dados.
    """
    dados = scrape_magazine_luiza(url)
    if dados:
        salvar_dados(dados, "magazine_luiza")
        ProdutoDAO.consolidar_dados()
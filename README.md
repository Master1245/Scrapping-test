# Projeto de Web Scraping, API e Agendamento com Celery

Este projeto implementa um sistema de coleta e consolidação de dados de ofertas de produtos dos marketplaces Amazon e Magazine Luiza. Os dados coletados são salvos em arquivos JSON, consolidados em um arquivo único e disponibilizados através de uma API REST construída com Flask. As tarefas de scraping são agendadas para execução periódica usando Celery e Celery Beat.

## Funcionalidades

- **Web Scraping**: Coleta ofertas de produtos na Amazon e Magazine Luiza.
- **Consolidação de Dados**: Salva os dados individuais em arquivos JSON e consolida todos em um único arquivo `produtos.json`.
- **API de Consulta**: API REST (Flask) que retorna os produtos consolidados ordenados pelo timestamp da coleta.
- **Agendamento de Tarefas**: Utiliza Celery e Celery Beat para executar as tarefas de scraping automaticamente a cada 1 minuto.
- **Containerização**: Projeto configurado para rodar em contêineres utilizando Docker e Docker Compose.

## Como executar 
    - Vamos criar uma venv com o comando: python python -m venv env
    - Vamos ativar a venv com o comando: env\Scripts\activate
    - Vamos agora instalar as dependencias com o comando: pip install -r requirements.txt
    - Vamos iniciar o docker
    - Logo apois iniciar o docker vamos dar o comando: docker-compose up --build
    - Logo apos aguardar 1 minutos os produtos vão aparecer na pasta data/produtos.json
    - Caso ache melhor visualizar em uma api só chamar o endpoint: http://localhost:5000/produtos
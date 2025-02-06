Projeto de Leitura de Notícias
Projeto para coletar notícias do site G1, armazenar em um banco de dados MySQL e exibir os dados em uma interface gráfica usando a biblioteca Flet.

Tecnologias Utilizadas
Python 3
Requests: Para fazer requisições HTTP.
BeautifulSoup4: Para extrair dados da página HTML.
MySQL Connector: Para se conectar e interagir com o banco de dados MySQL.
Flet: Para criar a interface gráfica de desktop.
Functools: Para funções parciais.
Pré-requisitos
Python 3 instalado
Banco de dados MySQL configurado
Instalar Dependências
bash
Copiar
pip install requests beautifulsoup4 mysql-connector-python flet
Configuração do Banco de Dados
Crie um banco de dados no MySQL chamado noticias_db:

sql
Copiar
CREATE DATABASE noticias_db;
Como Usar
Execute o script read.py:
bash
Copiar
python read.py
A interface gráfica será aberta com as 10 últimas notícias coletadas do G1.
Clique em "Ver detalhes" para ver mais informações sobre a notícia.
Banco de Dados
Tabela noticias:

Coluna	Tipo	Descrição
id	INT	Identificador único da notícia
titulo	TEXT	Título da notícia
data_extração	DATETIME	Data de extração da notícia

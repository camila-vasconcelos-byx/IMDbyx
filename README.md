# IMDbyx

Consiste em uma aplicação web em que usuários conseguem favoritar filmes, adicionar filmes a lista de filmes assistidos, adicionar filmes a lista de filmes que quer assistir, pesquisar por filmes e atores, ver detalhes de filmes e atores, filtrar filmes (gênero, ano de lançamento, ator do filme).

## Estrutura do Projeto
Tem dois aplicativos, IMDbyx, que contem a lógica principal do site, e users, que foi criado para fazer o controle de usuários (login, logout, criar usuários). 
A parte do frontend de cada aplicativo está na pasta "templates", para o HTML, e "static", para o CSS. Também há uma pasta "template" e uma pasta "static" fora dos aplicativos, que contém o HTML e CSS base da aplicação.

## Setup do projeto

### Pré-requisitos
```
- Python 3.10
- pip
```
### Instale as dependências 
```
pip install -r requirements.txt
```

### Faça as migrações
```
python manage.py makemigrations
python manage.py migrate
```

### Inicie o servidor
```
python manage.py runserver
```

## Tecnologias usadas
* Django Rest Framework: para construir a API
* Python: a linguagem de programação utilizada
* requests: biblioteca do Python para pegar os dados da API do TMDB
* PostgreSQL: banco de dados utilizado





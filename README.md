# Projeto Webscraping Betano

Visite minha documentacao

[![image](/pic/print.png)](https://igormartins0301.github.io/projeto-scraping-betano/)

## Pré-requisitos
1. Docker
2. MongoDBCompass

## Passos para executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/igormartins0301/projeto-scraping-betano.git
cd projeto-scraping-betano
```

2. Configure a versão correta do Python com `pyenv`:

```bash
pyenv install 3.11.3
pyenv local 3.11.3
```

3. Crie um ambiente virtual para o projeto:

```bash
python -m venv venv
venv/scripts/activate
```

4. Instale as dependencias do projeto:

```bash
pip install -r requirements.txt
```

5. Instale o MongoDB em sua máquina com Docker

```bash
docker compose up -d
```

6. Conecte o seu banco de dados criado no MongoDBCompass:

- No local de conexão coloque o URI: "mongodb://mongoadmin:secret@localhost:27017/"

- Após isso, crie um Database chamado "bet" e uma Collection chamada "betc".

7. Crie o seu arquivo .env baseado no .env-example, deixei o mesmo usuário e senha no exemplo do que foi criado via docker, portanto se quiser pode apenas mudar o nome do arquivo para .env

8. Execute o comando de execucão para extrair as odds e salvar no MongoDB:

```bash
python main.py
```
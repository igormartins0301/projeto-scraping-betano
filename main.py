from betCrawler.Browser.betanoCr import BetanoBrowser
from betCrawler.saveDatabase.mongoCr import MongoConnection

def main():
    # Configurações para exibir todas as linhas e colunas do DataFrame
    pd.set_option('display.max_rows', None)   
    pd.set_option('display.max_columns', None) 

    # Instanciando o navegador
    browser = BetanoBrowser()

    # Abrindo a URL desejada
    browser.open_url("https://br.betano.com/sport/futebol/brasil/brasileirao-serie-a/10016/")

    # Obtendo o HTML da página
    df = browser.get_html_from_url()

    # Procurando pelo texto 'Vasco' no HTML
    df_result = browser.search_text(text='Vasco', df=df)

    # Selecionando a seção principal do conteúdo
    df_result = browser.select_by_text(df=df_result, text='main-content')

    # Extraindo os jogos usando padrão regex
    jogos_extraidos = browser.extract_games(df=df_result, start='Escanteios', end='CUPOM DE APOSTAS', regex_pattern=r'\d{2}/\d{2}')

    # Convertendo os jogos extraídos para JSON
    json_list = browser.dataframe_to_json(dfs=jogos_extraidos)

    # Conectando ao banco de dados MongoDB
    mongo_conn = MongoConnection()

    # Escrevendo os dados no banco de dados
    for i in json_list:
        mongo_conn.write_mongo_db(i)

if __name__ == "__main__":
    main()

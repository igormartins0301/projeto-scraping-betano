from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
from PrettyColorPrinter import add_printer
import pandas as pd
from seleniumbase import Driver
from a_selenium2df import get_df
import json
from pymongo import MongoClient


add_printer(1)

class BetanoBrowser:
    def __init__(self):
        self.driver = Driver(uc=True)
        

    def open_url(self, url):
        """
        Abre uma URL no navegador.
        """
        self.driver.open(url)

    def get_html_from_url(self, query="*"):
        """
        Obtém o HTML da página e retorna as informações relevantes em um DataFrame.
        """
        df = pd.DataFrame()
        while df.empty:
            df = get_df(
                self.driver,
                By,
                WebDriverWait,
                expected_conditions,
                queryselector=query,
                with_methods=True,
            )
        return df
    
    def search_text(self, text, df):
        """
        Procura por um texto específico na coluna 'aa_innerText' do DataFrame e retorna as linhas correspondentes.
        """
        df_result = df[df['aa_innerText'].str.contains(text, regex=False, na=False) & (df['aa_tagName'] != 'DIV')]
        df_result = df_result[['aa_tagName', 'aa_innerText', 'aa_className']]
        return df_result
        
    def select_by_text(self, df, text):
        """
        Seleciona linhas do DataFrame com base no texto fornecido na coluna 'aa_className'.
        """
        text = df.loc[df.aa_className.str.contains(text, regex=False, na=False)].aa_innerText.iloc[0]
        df_filter = pd.DataFrame(text.splitlines())
        return df_filter
    
    def extract_games(self, df, start, end, regex_pattern):
        """
        Extrai os jogos do DataFrame com base nos padrões de início e fim fornecidos.
        """
        index_inicial = None
        index_final = None

        # Verifica se start e end não são None e atualiza os índices iniciais e finais
        if start:
            index_inicial = df.loc[df[0].str.contains(start, na=False, regex=False)].index[-1] + 1
        if end:
            index_final = df.loc[df[0].str.contains(end, na=False, regex=False)].index[-1]

        # Extrai os jogos com base nos índices iniciais e finais atualizados
        if index_inicial is not None and index_final is not None:
            df = df.iloc[index_inicial:index_final].reset_index(drop=True)
        elif index_inicial is not None:
            df = df.iloc[index_inicial:].reset_index(drop=True)
        elif index_final is not None:
            df = df.iloc[:index_final].reset_index(drop=True)

        
        
        df[0] = df[0].str.strip()

        indexes_data = df.loc[df[0].str.contains(regex_pattern, regex=True, na=False)].index
        allbets = [df.iloc[indexes_data[i]:indexes_data[i+1]] for i in range(len(indexes_data)-1)]
        df_append = df.iloc[indexes_data[-1]:].reset_index(drop=True)
        allbets.append(df_append)
        return allbets

    def dataframe_to_json(self, dfs):
        """
        Converte os DataFrames de jogos em uma lista de dicionários JSON.
        """
        colunas = {
            0: 'data',
            1: 'hora',
            2: 'mandante',
            3: 'visitante',
            5: 'odd_home',
            7: 'odd_draw',
            9: 'odd_away'
        }

        json_list = []

        for jogo in range(len(dfs)):
            json_data = {}

            for i, k in colunas.items():
                valor = dfs[jogo].iloc[i].values[0]
                json_data[k] = valor

            json_list.append(json_data)

        return json_list

import os
from pymongo import MongoClient
from dotenv import load_dotenv

class MongoConnection:
    def __init__(self):
        """
        Classe para gerenciar a conexão com o MongoDB e operações de escrita.

        Carrega as variáveis de ambiente do arquivo .env para estabelecer a conexão com o MongoDB.
        """
        load_dotenv()
        mongo_user = os.getenv("MONGODB_USER")
        mongo_password = os.getenv("MONGODB_PASSWORD")  
        mongo_host = os.getenv("MONGODB_HOST") 
        mongo_port = os.getenv("MONGODB_PORT") 
        
     
        self.URI = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
        self.client = MongoClient(self.URI)
        self.db = self.client['bet']
        self.collection = self.db['betc']
        
    def write_mongo_db(self, text):
        """
        Insere um documento na coleção 'betc' do MongoDB.

        Args:
            text (dict): O documento a ser inserido na coleção.
        """
        try:
            self.collection.insert_one(text)
            print('Documento inserido no MongoDB com sucesso')
        except Exception as e:
            print(f'Erro ao inserir documento no MongoDB: {str(e)}')

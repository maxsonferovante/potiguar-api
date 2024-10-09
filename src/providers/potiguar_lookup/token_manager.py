import json
import os
from datetime import datetime, timedelta
import jwt

class TokenManager:
    TOKEN_FILE = 'token_data.json'

    @staticmethod
    def is_token_valid():
        if not os.path.exists(TokenManager.TOKEN_FILE):
            return False

        # Carregar o token do arquivo JSON
        with open(TokenManager.TOKEN_FILE, 'r') as f:
            token_data = json.load(f)

        expiration_date = datetime.fromisoformat(token_data['expires_at'])

        # O token dura 10 minutos, mas caso falte 2 minutos para expirar, já é considerado inválido
        if expiration_date > datetime.now() - timedelta(minutes=2):
            return True
        return False

    @staticmethod
    def save_token(token):
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        # Pegar o tempo de expiração
        exp = decoded_token.get('exp')

        # Converter o tempo de expiração para formato legível (timestamp)
        expiration_time = datetime.utcfromtimestamp(exp).strftime('%Y-%m-%d %H:%M:%S')

        expiration_date = datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
        token_data = {
            'token': token,
            'expires_at': expiration_date.isoformat()  # Armazenar como string
        }

        # Salvar no arquivo JSON
        with open(TokenManager.TOKEN_FILE, 'w') as f:
            json.dump(token_data, f)

        
    @staticmethod
    def get_token():
        if TokenManager.is_token_valid():
            # Se o token ainda for válido, carregá-lo do arquivo
            with open(TokenManager.TOKEN_FILE, 'r') as f:
                token_data = json.load(f)

                return token_data['token']
        else:
            return None

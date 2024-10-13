import json
import os
from datetime import datetime, timedelta
import jwt

class TokenManager:
    TOKEN_FILE = 'token_data.json'
    AUTH_TOKEN = {
        "TOKEN": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMjI4NTQxODI0OCIsImp0aSI6IjUwZTIzMDZlLTI0OTUtNDYxNS05NGNmLWI4MDAwNzExNmFhMCIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IlQvVjY4WnFkcjV5eDhwcTZUb3dhL2NJbGF0ZDZsTllpWk1ocjFQMmdZMFhBTzN5dHhZbVdDcXg4RlFzVCtQNnNOQklCZkJJa1FDcHFEUEpmUXlsQ20zN0UzRFh0cEUwYUtWT1I0NDNJT3Bza0tLcG0zVU96L0ZoZEk2MjFvS2dzSVBRYzNnTnpCQ0UxNEd4NE9ia1ROZz09IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Ik1BWFNPTiBBTE1FSURBIEZFUk9WQU5URSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZ3JvdXBzaWQiOiJNZXVEZXRyYW4iLCJuYmYiOjE3Mjg4NTA2MzIsImV4cCI6MTcyODg1MTIzMiwiaXNzIjoiUG9ydGFsU2Vydmljb3MuU2VjdXJpdHkuQmVhcmVyIiwiYXVkIjoiUG9ydGFsU2Vydmljb3MuU2VjdXJpdHkuQmVhcmVyIn0.ufszZESDhJEPUZ5cLBz5oohyJN3PvhgkCdmX_OJwuNo',
        "EXPIRES_AT": '2024-10-01T17:37:12'
    }
    
    @staticmethod
    def is_token_valid():        
        expiration_date = datetime.fromisoformat(TokenManager.AUTH_TOKEN['EXPIRES_AT'])
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

        expiration_date = datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S')
        TokenManager.AUTH_TOKEN["TOKEN"] = token
        TokenManager.AUTH_TOKEN["EXPIRES_AT"] = expiration_date.isoformat()

        
    @staticmethod
    def get_token():
        if TokenManager.is_token_valid():
            # Se o token ainda for válido, carregá-lo do arquivo
            return TokenManager.AUTH_TOKEN["TOKEN"]
        else:
            return None


import os
from dotenv import load_dotenv
from nest.core.database.odm_provider import OdmProvider
from src.apps.order.order_entity import Order

load_dotenv()
config = OdmProvider(
    config_params={
        "db_name": os.getenv("DB_NAME", "default_nest_db"),
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "port": os.getenv("DB_PORT", 27017),
    },
    document_models=[Order],
)

config_recaptcha = {
    "key": os.getenv("RECAPTCHA_KEY", "RECAPTCHA_KEY"),
    "site_url": os.getenv("SITE_URL", "https://www.google.com"),
    "site_key": "6LdevPgfAAAAADYwit3dtW0Z5iC8K9_uzIHc-0Al",
    "url_captcha": os.getenv("URL_CAPTCHA", "https://api.capsolver.com"),
}

config_auth = {
    "username": os.getenv("AUTH_USERNAME", "admin"),    
    "password": os.getenv("AUTH_PASSWORD", "admin"),    
    "api": os.getenv("API_RN", "https://api.rn.gov.br"),
}

config_redis = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": os.getenv("REDIS_PORT", 6379),
    "password": os.getenv("REDIS_PASSWORD", ""),
    "url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
}
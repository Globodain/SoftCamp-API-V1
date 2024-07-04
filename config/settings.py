from pathlib import Path
from dotenv import load_dotenv
import os

class Config(object):
    def __init__(self, environment):
        self.environment = environment
        self.load_env_variables()
        self.set_environment()

    def load_env_variables(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.SECRET_KEY = os.getenv('SECRET_KEY')

        self.CSRF_ENABLED = False  # O el valor que desees por defecto
        self.WTF_CSRF_ENABLED = False  # O el valor que desees por defecto

        # Mailing
        self.MAIL_SERVER = 'smtp.sendgrid.net'
        self.MAIL_PORT = 587
        self.MAIL_USE_TLS = True
        self.MAIL_USE_SSL = False
        self.MAIL_USERNAME="ceo@weggo.es"
        self.MAIL_PASSWORD=os.getenv('SENDGRID_API_KEY')
        self.MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
        
        ## AWS BUCKET CONFIGURATION
        self.S3_BUCKET = os.getenv('S3_BUCKET')
        self.S3_LOCATION = os.getenv('S3_LOCATION')
        self.S3_KEY = os.getenv('S3_API_KEY')
        self.S3_SECRET = os.getenv('S3_API_SECRET_KEY')

        self.MONGO_URI_APP = os.getenv("DATABASE_TESTING_URL")
        self.MONGO_URI_API = os.getenv("API_DATABASE_LOCAL_URL")
        self.MONGO_URI_COMMUNITY = os.getenv("DATABASE_COMMUNITY_TESTING_URL")

        # Stripe API keys
        self.STRIPE_REAL_API_SECRET_KEY = os.getenv('STRIPE_REAL_API_SECRET_KEY')
        self.STRIPE_TEST_API_SECRET_KEY = os.getenv('STRIPE_TEST_API_SECRET_KEY')

    def set_environment(self):
        if self.environment == 'deployment':
            self.set_deployment_env()
        elif self.environment == 'testing':
            self.set_testing_env()
        else:
            self.set_default_env()

    def set_deployment_env(self):
        # Configuración para el entorno de despliegue
        self.ENV = "deployment"
        self.DEBUG = False
        self.CSRF_ENABLED = True
        self.WTF_CSRF_ENABLED = True
        self.BASE_URL = "https://api.softcamp.eu"
        
        self.MONGO_URI_APP = os.getenv("DATABASE_REMOTE_URL")
        self.MONGO_URI_API = os.getenv("API_DATABASE_DEPLOYMENT_URL")
        self.MONGO_URI_COMMUNITY = os.getenv("DATABASE_COMMUNITY_REMOTE_URL")

        self.SESSION_COOKIE_SECURE = True
        self.SESSION_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = 'SOFTCAMP'

        self.STRIPE_API_SECRET_KEY = self.STRIPE_REAL_API_SECRET_KEY

    def set_testing_env(self):
        # Configuración para el entorno de pruebas
        self.ENV = "testing"
        self.DEBUG = True
        self.BASE_URL = "http://localhost:8000"
        
        self.MONGO_URI_APP = os.getenv("DATABASE_TESTING_URL")
        self.MONGO_URI_API = os.getenv("API_DATABASE_TESTING_URL")
        self.MONGO_URI_COMMUNITY = os.getenv("DATABASE_COMMUNITY_TESTING_URL")

        self.STRIPE_API_SECRET_KEY = self.STRIPE_TEST_API_SECRET_KEY

    def set_default_env(self):
        # Configuración por defecto
        self.ENV = "development"
        self.DEBUG = True
        self.OAUTHLIB_INSECURE_TRANSPORT = True

        ## DATABASE MONGO URI
        self.MONGO_URI_APP = os.getenv("DATABASE_LOCAL_URL")
        self.MONGO_URI_API = os.getenv("API_DATABASE_LOCAL_URL")
        self.MONGO_URI_COMMUNITY = os.getenv("DATABASE_COMMUNITY_LOCAL_URL")

        self.STRIPE_API_SECRET_KEY = self.STRIPE_TEST_API_SECRET_KEY

    def update_app_config(self, app):
        app.config.update(
            DEBUG=self.DEBUG,
            FLASK_ENV=self.ENV,
            FLASK_APP=os.getenv('FLASK_APP'),
            SECRET_KEY=self.SECRET_KEY,
            BASE_URL = self.BASE_URL,
            MONGO_URI_APP=self.MONGO_URI_APP,
            MONGO_URI_API=self.MONGO_URI_API,
            MONGO_URI_COMMUNITY=self.MONGO_URI_COMMUNITY,
            CSRF_ENABLED=self.CSRF_ENABLED,
            WTF_CSRF_ENABLED=self.WTF_CSRF_ENABLED,
            MAIL_SERVER=self.MAIL_SERVER,
            MAIL_PORT=self.MAIL_PORT,
            MAIL_USE_TLS=self.MAIL_USE_TLS,
            MAIL_USERNAME=self.MAIL_USERNAME,
            MAIL_PASSWORD=self.MAIL_PASSWORD,
            MAIL_DEFAULT_SENDER=self.MAIL_DEFAULT_SENDER
        )
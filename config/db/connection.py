from config.settings import Config

instance = 'development' # Development, Testing, Deployment
config = Config(instance)

# Configuración de MongoDB
MONGO_URI_APP = config.MONGO_URI_APP
MONGO_URI_API = config.MONGO_URI_API
MONGO_URI_COMMUNITY = config.MONGO_URI_COMMUNITY

from pymongo import MongoClient
client_app = MongoClient(MONGO_URI_APP)
db_app = client_app.get_default_database()

client_community = MongoClient(MONGO_URI_COMMUNITY)
db_community = client_community.get_default_database()

client_api = MongoClient(MONGO_URI_API)
db_api = client_api.get_default_database()

# Configuración de CouchDB (sólo para datos offline y sincronización --> PouchDB)
# Añadido el update de la app en la clase Config

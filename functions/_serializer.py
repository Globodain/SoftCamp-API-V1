from auth._control import SECRET_KEY
from itsdangerous import URLSafeTimedSerializer

secret_key = SECRET_KEY

class Serializer:

    def URLSafeTimed():
        return URLSafeTimedSerializer(secret_key)
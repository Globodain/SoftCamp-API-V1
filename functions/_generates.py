import base64,os

class Generates:

    def salt(length):
        return base64.b64encode(os.urandom(length)).decode('utf-8')
from os import environ

CONN_STR = environ.get('CONN_STR')

SECRET_KEY = environ.get('SECRET_KEY')

ADMIN_MAIL = environ.get('ADMIN_MAIL')

MAIL_API_KEY = environ.get('MAIL_API_KEY')

MAIL_API_SECRET = environ.get('MAIL_API_SECRET')

COS_ENDPOINT = environ.get('COS_ENDPOINT')

COS_INSTANCE_CRN = environ.get('COS_INSTANCE_CRN')

COS_API_KEY_ID = environ.get('COS_API_KEY_ID')

COS_BUCKET_NAME = environ.get('COS_BUCKET_NAME')

COS_HMAC_ACCESS_KEY = environ.get('COS_HMAC_ACCESS_KEY')

COS_HMAC_SECRET_KEY = environ.get('COS_HMAC_SECRET_KEY')

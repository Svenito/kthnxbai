here = lambda * x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here('..')
root = lambda * x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

SECRET_KEY = "thisisasecret"
SESSION_COOKIE_NAME = "kthnxcookie"
DEBUG = False
PATH_TO_CONVERT = '/usr/bin/convert'
CSRF_ENABLED = True


IMAGE_PATH = "./static/images"
STATIC_URL = "/static/images/"

SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_ROOT, 'db_repository')
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/kthnxbai'

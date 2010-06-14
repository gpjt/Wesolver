# Local settings for development

from os.path import dirname, join, normpath

MY_DIR = dirname(__file__)
PYTHON_ROOT_DIR = normpath(join(MY_DIR, ".."))
TOP_ROOT_DIR = normpath(join(PYTHON_ROOT_DIR, ".."))

DB_FILE = join(PYTHON_ROOT_DIR, "dev.db")


DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'wesolver'          # Or path to database file if using sqlite3.
DATABASE_USER = 'wesolver_user'     # Not used with sqlite3.
DATABASE_PASSWORD = 's0lv31tt'      # Not used with sqlite3.
DATABASE_HOST = ''                  # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                  # Set to empty string for default. Not used with sqlite3.

ENVIRONMENT = "dmitri"
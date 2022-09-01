from distutils.command.config import config
import os

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

ROOT_DIR = os.getcwd()

conf = Config(f'{ROOT_DIR}/.env')

DATABASE_URL = f'sqlite:///{ROOT_DIR}/' + conf('DB_NAME', cast = str) + '?check_same_thread=False'

SECRET_KEY = conf('SECRET_KEY', cast=Secret)

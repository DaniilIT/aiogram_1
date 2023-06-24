from environs import Env

env = Env()
env.read_env()

LOG_LEVEL = env.log_level('LOG_LEVEL', default='INFO')
DB_ECHO = env.bool('DB_ECHO', default=False)
TG_TOKEN = env('TG_TOKEN')

DB_USER = env('DB_USER')
DB_PASS = env('DB_PASS')
DB_NAME = env('DB_NAME')
DB_HOST = env('DB_HOST', default='localhost')
DB_PORT = env('DB_PORT', default='5432')

REDIS_PASS = env('REDIS_PASS')
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')

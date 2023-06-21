from environs import Env

env = Env()
env.read_env()

LOG_LEVEL = env.log_level('LOG_LEVEL', default='INFO')
TG_TOKEN = env('TG_TOKEN')

DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_NAME = env('DB_NAME')
DB_HOST = env('DB_HOST', 'localhost')
DB_PORT = env('DB_PORT', '5432')

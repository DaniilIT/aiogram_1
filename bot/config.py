from environs import Env

env = Env()
env.read_env()

LOG_LEVEL = env.log_level('LOG_LEVEL', default='INFO')
TG_TOKEN = env('TG_TOKEN')

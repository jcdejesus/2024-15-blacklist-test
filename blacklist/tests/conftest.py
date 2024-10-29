import os

from dotenv import load_dotenv, find_dotenv

os.environ['ENV'] = 'test'
os.environ['FLASK_ENV'] = 'test'

def pytest_configure(config):
    env_file = find_dotenv('../.env.test')
    load_dotenv(env_file)
    return config

import json
import logging
import subprocess
from common import read_config
import os

configs = read_config('config/application.properties')
logger = logging.getLogger("sync_mysql")


def init_config():
    with open('config/mysql/mysql2mysql.json', 'r', encoding='utf-8') as file:
        template = file.read()
    template = json.loads(template)

    reader_params = template['job']['content']['reader']['parameter']
    reader_params['username'] = configs['mysql.0.username']
    reader_params['password'] = configs['mysql.0.password']
    reader_params['connection']['jdbcUrl'] = configs['mysql.0.url']

    writer_params = template['job']['content']['writer']['parameter']
    writer_params['username'] = configs['mysql.1.username']
    writer_params['password'] = configs['mysql.1.password']
    writer_params['connection']['jdbcUrl'] = configs['mysql.1.url']

    template = json.dumps(template, indent=4)
    tables = configs['mysql.sync.tables'].split(',')
    for table in tables:
        config = template.replace('$table', table)
        logger.info(f'job-config: {config}')
        config_file = format_config_file(table)
        with open(config_file, 'w', encoding='utf-8') as file:
            file.write(config)


def format_config_file(table):
    path = 'config/mysql/generated/'
    if not os.path.exists(path):
        os.mkdir(path)
    return f'{path}{table}.json'


def execute():
    tables = configs['mysql.sync.tables'].split(',')
    for table in tables:
        config_file = format_config_file(table)
        result = subprocess.run(['addax.sh', config_file], capture_output=True, text=True)
        logger.info(result)
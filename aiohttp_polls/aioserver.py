from aiomysql import connect
from aiohttp import web
from pathlib import Path
from yaml import safe_load

from views import mysql_get_handler


BASE_DIR = Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'polls.yaml'


def get_config(path):
    with open(path) as f:
        config = safe_load(f)
    return config


def setup_routes(app):
    app.router.add_get('/', mysql_get_handler)


async def init_mysql(app):
    config = app['config']['mysql']
    pool = await create_pool(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        db=config['database'],
        minsize=config['minsize'],
        maxsize=config['maxsize'],        
        )
    app['db'] = pool


async def close_mysql(app):
    app['db'].close()
    await app['db'].wait_closed()



logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename="log.json", level=logging.DEBUG)

app = web.Application()

config = get_config(config_path)
app['config'] = config
setup_routes(app)
app.on_startup.append(init_mysql)
app.on_cleanup.append(close_mysql)
web.run_app(app)

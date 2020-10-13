from aiomysql import connect
from aiohttp import web
from pathlib import Path
from yaml import safe_load

from views import index


BASE_DIR = Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'polls.yaml'


def get_config(path):
    with open(path) as f:
        config = safe_load(f)
    return config

def setup_routes(app):
    app.router.add_get('/', index)

async def init_mysql(app):
    conf = app['config']['mysql']
    engine = await connect(
        host=conf['host'],
        port=conf['port'],
        user=conf['user'],
        password=conf['password'],
        db=conf['database'],
    )
    app['db'] = engine	

async def close_mysql(app):
    app['db'].close()


app = web.Application()

config = get_config(config_path)
app['config'] = config

setup_routes(app)

app.on_startup.append(init_mysql)
# app.on_cleanup.append(app.close())
# app['db'].close()
app.on_cleanup.append(close_mysql)
print(type(close_mysql))
web.run_app(app)


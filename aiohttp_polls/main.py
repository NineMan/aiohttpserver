from aiohttp import web
import logging

from settings import config
from routes import setup_routes
from db import init_mysql
from db import close_mysql



logging.basicConfig(level=logging.DEBUG)
app = web.Application()
app['config'] = config
setup_routes(app)
app.on_startup.append(init_mysql)
app.on_cleanup.append(close_mysql)
web.run_app(app)

from aiohttp import web
from aiohttp import web_app
import logging

from settings import config
from routes import setup_routes
from db import init_mysql
from db import close_mysql


logging.basicConfig(
    level=logging.DEBUG,
    filename="log.json",
    format='%(asctime)s %(name)-14s %(levelname)-8s:: %(message)s',
    )


app = web.Application()
app['config'] = config
setup_routes(app)
app.on_startup.append(init_mysql)
app.on_cleanup.append(close_mysql)
web.run_app(app, access_log_format="%s %r")

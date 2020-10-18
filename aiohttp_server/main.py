from aiohttp import web
import logging

from settings import config
from routes import setup_routes
from db import init_mysql
from db import init_redis
from db import close_mysql
from db import close_redis


logging.basicConfig(
    level=logging.DEBUG,
    filename="server.log",
    format='%(asctime)s %(name)-14s %(levelname)-8s:: %(message)s',
    )


app = web.Application()
app['config'] = config
setup_routes(app)
app.on_startup.append(init_mysql)
app.on_startup.append(init_redis)
app.on_cleanup.append(close_mysql)
app.on_cleanup.append(close_redis)
web.run_app(app, access_log_format="%s %r")

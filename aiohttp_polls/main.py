from aiohttp import web

from settings import config
from routes import setup_routes
from db import init_mysql
from db import close_mysql



app = web.Application()
app['config'] = config
setup_routes(app)
app.on_startup.append(init_mysql)
app.on_cleanup.append(close_mysql)
web.run_app(app)

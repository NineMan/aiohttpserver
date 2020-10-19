from views import mysql_get_handler
from views import mysql_post_handler
from views import mysql_delete_handler
from views import log_get_handler
from views import redis_get_handler
from views import redis_post_handler


def setup_routes(app):
    app.router.add_get("/mysql", mysql_get_handler)
    app.router.add_post("/mysql", mysql_post_handler)
    app.router.add_delete("/mysql", mysql_delete_handler)
    app.router.add_get("/log", log_get_handler)
    app.router.add_get("/redis", redis_get_handler)
    app.router.add_post("/redis", redis_post_handler)

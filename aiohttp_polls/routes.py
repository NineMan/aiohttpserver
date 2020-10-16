from views import mysql_get_handler
from views import mysql_post_handler
from views import mysql_delete_handler


def setup_routes(app):
    app.router.add_get('/', mysql_get_handler)
    app.router.add_post('/', mysql_post_handler)
    app.router.add_delete('/', mysql_delete_handler)

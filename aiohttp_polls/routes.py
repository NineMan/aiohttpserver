from views import mysql_get_handler

def setup_routes(app):
    app.router.add_get('/', mysql_get_handler)

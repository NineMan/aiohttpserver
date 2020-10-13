from aiomysql import connect


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
#     await app['db'].wait_closed()

from aiomysql import create_pool
import asyncio


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

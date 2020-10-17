from aiomysql import create_pool
import asyncio
import aioredis


async def init_mysql(app):
    config = app['config']['mysql']
    pool_mysql = await create_pool(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        db=config['database'],
        )
    app['db_mysql'] = pool_mysql


async def init_redis(app):
    config = app['config']['redis']
    pool_redis = await aioredis.create_redis_pool(
        (config['host'], config['port'])
        )
    app['db_redis'] = pool_redis


async def close_mysql(app):
    app['db_mysql'].close()
    await app['db_mysql'].wait_closed()


async def close_redis(app):
    app['db_redis'].close()
    await app['db_redis'].wait_closed()

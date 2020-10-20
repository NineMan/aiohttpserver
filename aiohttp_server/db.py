from aiomysql import create_pool
import asyncio
import aioredis


# List fields of product in MySQL
FIELDS = ["id", "product_name", "description", "value"]

# Set of saved products in Redis (product_hash)
NAME_OF_SET = 'products'


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


async def fetch_mysql(query, pool):
    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query)
                records = await cursor.fetchall()
                return records
    except Exception:
        return False


async def commit_mysql(query, pool):

    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query)
                await connection.commit()
                return True

    except Exception as e:
        return False


async def hashget_redis(pool):

    try:
        with await pool as connection:
            product_hashes = await connection.execute("smembers", NAME_OF_SET)
            response = []

            for product_hash in product_hashes:
                keys_values = await connection.execute("hgetall", product_hash)

                resp = {}
                for i in range(0, len(keys_values), 2):
                    key = keys_values[i].decode("utf-8")
                    val = keys_values[i + 1].decode("utf-8")
                    resp[key] = val
                resp["value"] = int(resp["value"])
                response.append(resp)
                return response
    except Exception:
        return False


async def hashadd_redis(key, request, pool):

    try:
        with await pool as connection:
            for field, value in request.items():
                await connection.execute("hset", key, field, value)
                await connection.execute("sadd", NAME_OF_SET, key)
            return True

    except Exception:
        return False

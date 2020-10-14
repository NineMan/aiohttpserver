from aiohttp import web
import db
import logging


async def mysql_get_handler(request):
    async with request.app['db'].acquire() as connection:
        async with connection.cursor() as cursor:
            query = "SELECT id, product_name, description, value FROM neovox_products"
            await cursor.execute(query)
            records = await cursor.fetchall()

            answer = ''
            for record in records:
                answer = answer + ' : '.join(map(str, record)) + '\n'

    return web.Response(text=answer)


async def mysql_post_handler(request):
    pass


async def redis_get_handler(request):
    pass


async def redis_post_handler(request):
    pass

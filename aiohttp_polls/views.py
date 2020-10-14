from aiohttp import web
import db
import logging


async def mysql_get_handler(request):
    async with request.app['db'].acquire() as connection:
        async with connection.cursor() as cursor:
            query = "SELECT email, password FROM users"
            await cursor.execute(query)
            records = await cursor.fetchall()

            answer = ''
            for record in records:
                for field in record:
                    answer += field + ' '
                answer += '\n'

    return web.Response(text=answer)


async def mysql_post_handler(request):
    pass


async def redis_get_handler(request):
    pass


async def redis_post_handler(request):
    pass

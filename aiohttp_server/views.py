from aiohttp import web
import json
import aiofiles


PRODUCT = ['id', 'product_name', 'description', 'value']


async def mysql_get_handler(request):
    async with request.app['db_mysql'].acquire() as connection:
        async with connection.cursor() as cursor:
            query = "SELECT id, product_name, description, value FROM neovox_products"
            await cursor.execute(query)
            records = await cursor.fetchall()

            response = []
            for record in records:
                resp = dict(zip(PRODUCT, record))
                response.append(resp)
            return web.json_response(response)


async def mysql_post_handler(request):
    if request.method == 'POST':
        async with request.app['db_mysql'].acquire() as connection:
            async with connection.cursor() as cursor:

                request_json = await request.json()

                if PRODUCT[1] in request_json:
                    product_name = request_json[PRODUCT[1]].strip()
                else:
                    product_name = None

                if PRODUCT[2] in request_json:
                    description = request_json[PRODUCT[2]].strip()
                else:
                    description = None

                if PRODUCT[3] in request_json:
                    value = request_json[PRODUCT[3]]
                    if not isinstance(value, int):
                        return web.json_response({
                            "Error": "'value' must be a number"
                            })
                else:
                    value = None

                if (product_name is None) or (description is None) or (value is None):
                    return web.json_response({
                        "Error": "Product_name, description and value required field"
                        })

                await cursor.execute(
                    f"INSERT neovox_products (product_name, description, value) "
                    f"VALUES ('{product_name}', '{description}', {value})"
                )
                await connection.commit()

                data = {"status": 200, "data": {"product_name": product_name, "description": description, "value": value}}
                with open('log.json', mode='a', encoding='utf-8') as file:
                    json.dump(data, file)
                    file.write('\n')

                return web.json_response({
                    "Success": "INSERT executed successfully"
                    })

    return web.json_response({
        "Error": "INSERT finished with error"
        })


async def mysql_delete_handler(request):
    async with request.app['db_mysql'].acquire() as connection:
        async with connection.cursor() as cursor:

            if request.can_read_body:
                request_json = await request.json()
                if PRODUCT[1] in request_json:
                    product_name = request_json[PRODUCT[1]].strip()
                else:
                    product_name = 'product'            # default product_name 
                    #return web.json_response({
                    #    "Error": "Product name are required"
                    #    })
            else:
                return web.json_response({
                    "Error": "Request is empty"
                    })

            query = f"DELETE FROM neovox_products WHERE product_name='{product_name}'"
            await cursor.execute(query)
            await connection.commit()
    return web.json_response({
        "Success": "DELETE executed successfully"
        })


async def log_get_handler(request):
    async with aiofiles.open('log.json', mode='r', encoding='utf-8') as f:
        resp = []
        async for line in f:
            line = json.loads(line[:-1])
            resp.append(line)

    return web.json_response(resp)


async def redis_get_handler(request):

    with await request.app['db_redis'] as connection:
        await connection.execute('set', 'my-key', 'value')
        val = await connection.execute('get', 'my-key')

    print('raw value:', val)

    return web.json_response({
        "Success": "Redis executed"
        })


async def redis_post_handler(request):
    pass

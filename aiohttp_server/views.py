from aiofile import AIOFile
from aiofile import LineReader
from aiofile import Writer
from aiohttp import web
from json import dumps
from json import loads


FIELDS = ["id", "product_name", "description", "value"]


async def mysql_get_handler(request):

    async with request.app["db_mysql"].acquire() as connection:
        async with connection.cursor() as cursor:
            query = "SELECT id, product_name, description, value FROM neovox_products"
            await cursor.execute(query)
            records = await cursor.fetchall()

            response = []
            for record in records:
                resp = dict(zip(FIELDS, record))
                response.append(resp)

            return web.json_response(response, status=200)


async def mysql_post_handler(request):
    if request.method == "POST":

        request_json = await request.json()

        if FIELDS[1] in request_json:
            product_name = request_json[FIELDS[1]].strip()
        else:
            product_name = None

        if FIELDS[2] in request_json:
            description = request_json[FIELDS[2]].strip()
        else:
            description = None

        if FIELDS[3] in request_json:
            value = request_json[FIELDS[3]]
            if not isinstance(value, int):
                return web.json_response(
                    {"Error": "value must be a number"},
                    status=400
                    )
        else:
            value = None

        if (product_name is None) or (description is None) or (value is None):
            return web.json_response(
                {"Error": "Product_name, description and value required field"},
                status=400
                )

        async with request.app["db_mysql"].acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    f"INSERT neovox_products (product_name, description, value) "
                    f"VALUES ('{product_name}', '{description}', {value})"
                )
                await connection.commit()

                data = {"status": 200,
                        "data": {
                            "product_name": product_name,
                            "description": description,
                            "value": value
                        }}
                data = dumps(data) + "\n"

                async with AIOFile("log.json", "a") as afp:
                     writer = Writer(afp)
                     await writer(data)

                return web.json_response(
                    {"Success": "MySQL INSERT executed successfully"},
                    status=200
                    )
    return web.json_response(
        {"Error": "Need POST request"},
        status=400
        )


async def mysql_delete_handler(request):

    if request.can_read_body:
        request_json = await request.json()
        if FIELDS[1] in request_json:
            product_name = request_json[FIELDS[1]].strip()
        else:
            #product_name = "product"            # set default product_name for developing
            return web.json_response(
                {"Error": "Product name are required"},
                status=400
                )
    else:
        return web.json_response(
            {"Error": "Request is empty"},
            status=400
            )

    async with request.app["db_mysql"].acquire() as connection:
        async with connection.cursor() as cursor:
            query = f"DELETE FROM neovox_products WHERE product_name='{product_name}'"
            await cursor.execute(query)
            await connection.commit()

    return web.json_response(
        {"Success": "MySQL DELETE executed successfully"},
        status=200
        )


async def log_get_handler(request):

    # Return response as text
    async with AIOFile("log.json", "r") as afp:
        response = ""
        async for line in LineReader(afp):
            response = response + line
    return web.Response(text=response, status=200)

#    # Return response as json
#    async with AIOFile("log.json", "r") as afp:
#        response = []
#        async for line in LineReader(afp):
#            string = loads(line)
#            response.append(string)
#    return web.json_response(response, status=200)


async def redis_get_handler(request):
    with await request.app["db_redis"] as connection:
        product_hashes = await connection.execute("smembers", "products")
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

    return web.json_response(response, status=200)


async def redis_post_handler(request):
    if request.method == "POST":

        request_json = await request.json()

        if FIELDS[1] in request_json:
            key = request_json[FIELDS[1]].strip()
        else:
            return web.json_response(
                {"Error": "Product name are required"},
                status=400
                )

        for field in request_json:
            with await request.app["db_redis"] as connection:
                await connection.execute("hset", key, field, request_json[field])
                await connection.execute("sadd", "products", key)

        data = {"status": 200, "data": request_json}
        data = dumps(data) + "\n"
        async with AIOFile("log.json", "a") as afp:
            writer = Writer(afp)
            await writer(data)

        return web.json_response(
            {"Success": "Redis SET executed successfully"},
            status=200
            )

    return web.json_response(
        {"Error": "Need POST request"},
        status=400
        )

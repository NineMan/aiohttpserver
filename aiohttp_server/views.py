from aiofile import AIOFile
from aiofile import LineReader
from aiohttp import web
from json import dumps
from json import loads
from db import fetch_mysql, commit_mysql
from db import hashget_redis, hashadd_redis
from db import FIELDS



async def mysql_get_handler(request):

    query = "SELECT id, product_name, description, value FROM neovox_products"
    pool_connections = request.app["db_mysql"]

    records = await fetch_mysql(query, pool_connections)

    if records:
        answer = []
        for record in records:
            resp = dict(zip(FIELDS, record))
            answer.append(resp)
        response = answer, 200
        await write_log(request, response)
        return web.json_response(response[0], status=response[1])
    else:
        response = {"Error": "MySQL SELECT not executed"}, 400
        await write_log(request, response)
        return web.json_response(response[0], status=response[1])


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
                response = {"Error": "value must be a number"}, 400
                await write_log(request, response)
                return web.json_response(response[0], status=response[1])
        else:
            value = None

        if (product_name is None) or (description is None) or (value is None):
            response = {"Error": "Product_name, description and value required field"}, 400
            await write_log(request, response)
            return web.json_response(response[0], status=response[1])

        query = f"INSERT neovox_products (product_name, description, value) " \
                f"VALUES ('{product_name}', '{description}', {value})"
        pool_connections = request.app["db_mysql"]
        ans = await commit_mysql(query, pool_connections)

        if ans:
            resp_log = request_json, 200
            resp_web = {"Success": "MySQL INSERT executed successfully"}, 200
            await write_log(request, resp_log)
            return web.json_response(resp_web[0], status=resp_web[1])

        resp_log = request_json, 400
        resp_web = {"Error": "MySQL INSERT not executed"}, 400
        await write_log(request, resp_log)
        return web.json_response(resp_web[0], status=resp_web[1])


async def mysql_delete_handler(request):

    if request.can_read_body:
        request_json = await request.json()
        if FIELDS[1] in request_json:
            product_name = request_json[FIELDS[1]].strip()
        else:
            response = {"Error": "Product name are required"}, 400
            await write_log(request, response)
            return web.json_response(response[0], status=response[1])
    else:
        response = {"Error": "Request is empty"}, 400
        await write_log(request, response)
        return web.json_response(response[0], status=response[1])

    query = f"DELETE FROM neovox_products WHERE product_name='{product_name}'"
    pool_connections = request.app["db_mysql"]

    ans = await commit_mysql(query, pool_connections)

    if ans:
        resp_log = request_json, 200
        resp_web = {"Success": "MySQL DELETE executed successfully"}, 200
        await write_log(request, resp_log)
        return web.json_response(resp_web[0], status=resp_web[1])

    resp_log = request_json, 400
    resp_web = {"Error": "MySQL DELETE not executed"}, 400
    await write_log(request, resp_log)
    return web.json_response(resp_web[0], status=resp_web[1])


async def redis_get_handler(request):
    pool_connection = request.app["db_redis"]
    answer = await hashget_redis(pool_connection)

    if answer:
        response = answer, 200
        await write_log(request, response)
        return web.json_response(response[0], status=response[1])
    else:
        response = {"Error": "Redis GET not executed"}, 400
        await write_log(request, response)
        return web.json_response(response[0], status=response[1])


async def redis_post_handler(request):

    if request.method == "POST":

        request_json = await request.json()

        if FIELDS[1] in request_json:
            key = request_json[FIELDS[1]].strip()
        else:
            resp_log = request_json, 400
            resp_web = {"Error": "Product_name are required"}, 400
            await write_log(request, resp_log)
            return web.json_response(resp_web[0], status=resp_web[1])

        pool_conn = request.app["db_redis"]
        resp = await hashadd_redis(key, request_json, pool_conn)

        if resp:
            resp_log = request_json, 200
            resp_web = {"Success": "Redis HASHSET executed successfully"}, 200
            await write_log(request, resp_log)
            return web.json_response(resp_web[0], status=resp_web[1])

        resp_log = request_json, 400
        resp_web = {"Error": "Redis HASHSET not executed"}, 400
        await write_log(request, resp_log)
        return web.json_response(resp_web[0], status=resp_web[1])


async def write_log(request, response, file="log.json"):

    try:
        log = {
            "status": response[1],
            "method": request.method,
            "path": request.path,
            "data": response[0]
        }
        log = dumps(log) + "\n"

        async with AIOFile(file, "a") as afp:
            await afp.write(log)
            await afp.fsync()
        return True

    except Exception:
        return False


async def log_get_handler(request):

    try:
        async with AIOFile("log.json", "r") as afp:
            response = []
            async for line in LineReader(afp):
                string = loads(line)
                response.append(string)

        resp_log = "No data", 200
        resp_web = response, 200
        await write_log(request, resp_log)
        return web.json_response(resp_web[0], status=resp_web[1])

    except Exception:
        resp_log = "No data", 400
        resp_web = {"Error": "Log.json is not read"}, 400
        await write_log(request, resp_log)
        return web.json_response(resp_web[0], status=resp_web[1])

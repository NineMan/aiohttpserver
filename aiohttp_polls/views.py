from aiohttp import web
import db
import logging



async def index(request):
    async with request.app['db'] as connection:
        
#        logging.basicConfig(level=logging.INFO, 
#                            filename='app.log', 
#                            filemode='w', 
#                            format='%(name)s - %(levelname)s - %(message)s')
        
        cursor = await connection.cursor()
        await cursor.execute("SELECT email, password FROM users")
        records = await cursor.fetchall()
#        print(records)
#        print(type(records))
        answer = ''
        for record in records:
            for field in record:
                answer += field + ' '
            answer += '\n'
        print('answer =', answer)
        return web.Response(text=answer)

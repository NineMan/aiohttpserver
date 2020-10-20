**Aiohttp_server**
===

GET, POST, DELETE methods at `/mysql` are implemented for MySQL.

For Redis the methods of GET, POST at `/redis` are implemented.

The GET method at: `/log` is implemented to obtain logs.

The file `log.json` stores json with information about the status of the answer, method, URL 
and the sent/received data (json) of the request.

Answers are given by json.

The MySQL database uses a table: 

`products` with fields 
    
    id, 
    product_name, 
    description, 
    value

The Redis database will store json with data similar to that in MySQL. 

Translated with www.DeepL.com/Translator (free version)


**Hou run**
===

Create and activate virtual environment:

```
virtualenv -p python3 virtenv
source virtenv/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

You need running MySQL server. 

In 'init_db.py' set up USER and PASSWORD of MySQL

Next - create and content MySQL database

```
python init_db.py
```

Run aiohttp application:

```
python aiohttp_polls/main.py
```

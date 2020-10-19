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

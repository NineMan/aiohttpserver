import pymysql.cursors


USER = 'root'
PASSWORD = 'Yjdjcb,bhcr123'

# Create database, user, grant user
connection = pymysql.connect(host='localhost',
                             user=USER,
                             password=PASSWORD)
try:
    with connection.cursor() as cursor:
        cursor.execute("DROP DATABASE IF EXISTS neovox_test")
        cursor.execute("CREATE DATABASE neovox_test")
        cursor.execute("DROP USER 'neovox_user'@'localhost'")
        cursor.execute("CREATE USER 'neovox_user'@'localhost' IDENTIFIED BY 'neovox_pass'")
        cursor.execute("GRANT ALL ON neovox_test.* TO 'neovox_user'@'localhost'")
        connection.commit()
finally:
    connection.close()


# Create table and data i table
connection = pymysql.connect(host='localhost',
                             user='neovox_user',
                             password='neovox_pass',
                             db='neovox_test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:

        drop_table = "DROP TABLE IF EXISTS neovox_products"
        cursor.execute(drop_table)
        cursor.execute("""
            CREATE TABLE neovox_products (
            id INT NOT NULL AUTO_INCREMENT,
            product_name VARCHAR(30) NOT NULL,
            description VARCHAR(200),
            value INT DEFAULT 0,            
            PRIMARY KEY (id))""")
        connection.commit()

        sqls = (
            "INSERT neovox_products (product_name, description, value) VALUES ('Laptop', 'Is a small portable personal computer', 1)",
            "INSERT neovox_products (product_name, description, value) VALUES ('Mobile phone', 'Portable telephone ', 1)",
            "INSERT neovox_products (product_name, description, value) VALUES ('Headset', 'Communication accessor', 1)"
            )

        for sql in sqls:
            cursor.execute(sql)

        connection.commit()

finally:
    connection.close()


# FINISH:

# DROP DATABASE IF EXISTS neovox_test;
# CREATE DATABASE neovox_test;

# DROP USER 'neovox_user'@'localhost';
# CREATE USER 'neovox_user'@'localhost' IDENTIFIED BY 'neovox_pass';
# GRANT ALL ON neovox_test.* TO 'neovox_user'@'localhost';

# CREATE TABLE neovox_products (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, product_name VARCHAR(30) NOT NULL, description VARCHAR(200), value INT DEFAULT 0);

# INSERT neovox_products (product_name, description, value) VALUES ('Laptop', 'Is a small portable personal computer', 1);
# INSERT neovox_products (product_name, description, value) VALUES ('Mobile phone', 'Portable telephone', 1);
# INSERT neovox_products (product_name, description, value) VALUES ('Headset', 'Communication accessory', 1);

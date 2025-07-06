import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='bot_users',
        cursorclass=pymysql.cursors.DictCursor  
    )

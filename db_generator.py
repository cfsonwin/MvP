import pymysql

from MyProduct.settings import DATABASES

file_path = r'SQL_script/createtable.sql'
default_db = DATABASES['default']
try:
    database = {
        'user': default_db['USER'],
        'password': default_db['PASSWORD'],
        'host': default_db['HOST'],
        'port': int(default_db['PORT']),
    }
    db_name = default_db['NAME']
    db = pymysql.connect(**database, charset='utf8')
    cursor = db.cursor()
    with open(file_path) as f:
        line_list = f.read().split(';')[:-1]
        for line in line_list:
            newline = line.replace('DB_NAME', db_name)
            if '\n' in newline:
                newline = newline.replace('\n', '')
            sql_line = newline + ';'
            cursor.execute(sql_line.encode('utf8'))
except Exception as Err:
    print('err occured:', Err)
finally:
    cursor.close()
    db.commit()
    db.close()


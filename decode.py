file_path = r'SQL_script/data.sql'
with open(file_path) as f:
    line_list = f.read().split(';')[:-1]
    for line in line_list:
        newline = line.replace('DB_NAME', 'test')
        if '\n' in newline:
            newline = newline.replace('\n', '')
        sql_line = newline + ';'
        sql_utf8 = sql_line.encode('utf8')
        print(sql_line)
        print(sql_utf8)

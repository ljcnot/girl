import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lw930522',db='girl')
cur = conn.cursor()
url = "www.ugirl.com"
sql = "INSERT INTO stanpath_table(stanPath)VALUES(\'"+url+"\')"
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
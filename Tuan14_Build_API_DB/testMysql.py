import mysql.connector

cnx = mysql.connector.connect(user='root', password='psw123', port='6603',
                              host='127.0.0.1',
                              database='local_db')
cursor = cnx.cursor()
table_name = 'books'

add_book = (f"INSERT INTO {table_name} "
               "(title, price) "
               "VALUES (%s, %s)")
data_book = ('Conan', '300')

cursor.execute(add_book, data_book)

cnx.commit() # lưu những dữ liệu chúng ta đã chèn vào DB
cursor.close()
cnx.close()

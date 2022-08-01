from logging import error
from pymysql import MySQLError
import pymysql.cursors

class DB():
    def __init__(self):
        self.connection=pymysql.connect(host='localhost',user='root',password='',db='lab',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    
    def query(self,sql,select):
        try:
            #從數據庫鏈接中得到cursor的數據結構
            with self.connection.cursor() as cursor:
                #在之前建立的user表格基礎上，插入新數據，這裡使用了一個預編譯的小技巧，避免每次都要重複寫sql的語句
                #uPassword:預設a加學號
                cursor.execute(sql)
                #執行到這一行指令時才是真正改變了數據庫，之前只是緩存在內存中
        except MySQLError:
            print("sql error")
        finally:
            if select==True:
                return cursor.fetchall()
            self.connection.commit()
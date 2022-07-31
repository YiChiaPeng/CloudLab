
'''
這裡放http登陸驗證

'''
from pymysql import MySQLError
import pymysql.cursors
class Varify:
    @auth.get_password
    def get_password(uId):
        
        connection=pymysql.connect(host='localhost',user='root',password='',db='lab',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        try:
            #從數據庫鏈接中得到cursor的數據結構
            with connection.cursor() as cursor:
                #在之前建立的user表格基礎上，插入新數據，這裡使用了一個預編譯的小技巧，避免每次都要重複寫sql的語句
                sql="SELECT `uPassword` FROM `user` WHERE `uId`=%s"
                #uPassword:預設a加學號
                cursor.execute(sql,(uId))
                #執行到這一行指令時才是真正改變了數據庫，之前只是緩存在內存中
        except MySQLError:
            print("sql error")
        finally:
            connection.commit()
            result = cursor.fetchone()
            return result
 
    @auth.error_handler
    def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 401)
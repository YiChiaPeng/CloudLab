'''
更改一個User的resource
及提供的function
'''
from email import parser
from flask import jsonify
from flask_restful import Resource
from common.DBhandler import DBhandler
from flask_restful import reqparse
'''
我參考的命名規則
==========  =====================  ==================================
HTTP 方法   行为                   示例
==========  =====================  ==================================
GET         获取资源的信息         http://example.com/api/orders
GET         获取某个特定资源的信息 http://example.com/api/orders/123
POST        创建新资源             http://example.com/api/orders
PUT         更新资源               http://example.com/api/orders/123
DELETE      删除资源               http://example.com/api/orders/123
==========  ====================== ==================================
'''
class User(Resource):
    
    
    '''
    要登陸才能執行
    把所有資料庫的user讀出出來
    '''
    def __init__(self) -> None:
        #繼承上層Resource的init
        super().__init__()  
        self.db_handler=DBhandler()
    
           
    def get(self,id):
        results=self.db_handler.query("SELECT * FROM `user` WHERE `uId`={}".format(id),True)
        return jsonify(results[0])
            
        
        
    
    
    def post(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('uId', required=True)
        parser.add_argument('uName', required=True)
        arg=parser.parse_args()
        sql="INSERT INTO `user`(`uId`,`uPassword`,`uName`,`uPrivilege`) VALUES (\"{}\",\"{}\",\"{}\",\"{}\")".format(arg['uId'],"a"+arg['uId'],arg['uName'],'0')
        self.db_handler.query(sql,False)

        

    def put_users(self, uId,uName):
        connection=pymysql.connect(host='localhost',user='root',password='',db='lab',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    
        try:
            #從數據庫鏈接中得到cursor的數據結構
            with connection.cursor() as cursor:
                #在之前建立的user表格基礎上，插入新數據，這裡使用了一個預編譯的小技巧，避免每次都要重複寫sql的語句
                sql="INSERT INTO `user`(`uId`,`uPassword`,`uName`,`uPrivilege`) VALUES (%s,%s,%s,%s)"
                #uPassword:預設a加學號
                cursor.execute(sql,(uId,'a'+uId,uName,int()))
                #執行到這一行指令時才是真正改變了數據庫，之前只是緩存在內存中
        finally:
            connection.commit()


    def delete(self, name):
        global users
        users = [item for item in users if item['name'] != name]
        return {
            'message': 'Delete done!'
        }
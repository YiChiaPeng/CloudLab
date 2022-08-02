'''
更改一個User的resource
及提供的function
'''
from flask import jsonify
from flask_restful import Resource
from common.DBhandler import DBhandler
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
    
    def get(self,id=0):
        if id!=0:
            results=self.db_handler.query("SELECT * FROM `user` WHERE `uId`={}".format(id),True)
            return jsonify(results[0])
        else:
            results=self.db_handler.query("SELECT * FROM `user`",True)
            #有多筆資料
            items={}
            for i in range(0,len(results)):
                items.update({i:results[i]})
                return jsonify(items)
            
        
        
    
    
    def post(self, filename):
        pass

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
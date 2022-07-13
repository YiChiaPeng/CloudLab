import pymysql
import csv

'''
匯入csv檔
到sql
'''
def import_user(file_name):
    # 開啟 CSV 檔案
    with open('./user.csv', newline='') as csvfile:

        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)

        # 以迴圈輸出每一列
        for row in rows:
            print(row)
if __name__=='__main__':
    import_user("./user.csv")
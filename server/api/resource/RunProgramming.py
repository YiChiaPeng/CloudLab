from asyncio.subprocess import PIPE
from flask import Flask, request
from flask_restful import Resource, Api
from subprocess import PIPE
import subprocess
import time

app = Flask(__name__)
api = Api(app)

class RunProgramming(Resource):
    '''
    上傳完PGV和SOF檔之後，傳兩個檔案的路徑和檔案名稱給這個api，之後就會燒程式進去DE0然後回傳law檔案回去
    Inputs:
        codePath:有PGV和SOF檔的檔案路徑
        pgvName:向量檔的檔案名稱
        sofName:sof檔的檔案名稱
    Outputs:
        law file:燒錄完的波型檔
    '''
    def get(self):
        return {'Msg': 'This is GET method!'}
    def post(self):
        pgvDataPath = request.get_json()
        print(pgvDataPath['codePath'])
        batPath = "C:\\git-repos\\ours\\CloudLab\\server\\api\\common\\"

        # batPath = "..\\common\\PG_run.bat"

        ###write PG_run bat file
        with open(pgvDataPath['codePath'] + "\\" + pgvDataPath['pgvName'],'r') as f:
            data = f.read()

            data = data.strip()
            # print(data)
            tmp = data.splitlines()

            timeUnit = tmp[3]
            timeUnit = timeUnit.strip()[5] #取得時間單位
            # print(tmp)

            #取得輸出波型需要幾秒
            if(len(tmp[-1]) == 1):
                wtime = tmp[-2]
            else:
                wtime = tmp[-1]
            wtime = wtime[:wtime.rfind('>')].strip()

            #算出需要多少ms輸出波型
            if timeUnit == 'N' or timeUnit == 'n':
                waveTime = float(wtime) * pow(10,-6)
            if timeUnit == 'U' or timeUnit == 'u':
                waveTime = float(wtime) * pow(10,-3)
            if timeUnit == 'M' or timeUnit == 'm':
                waveTime = float(wtime)

            print("Time is {}ms".format(str(waveTime)))


        with open(batPath + "PG_run.bat",'w') as fileWrite:
            fileWrite.write("cd " + pgvDataPath['codePath'])
            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\PG_run\\bin\\x86\\Debug\\PG_1.exe {} {}".format(pgvDataPath['pgvName'],str(waveTime)))
        ###
        
        ### write Quartus programming bat file
        with open(batPath + "Programming_run.bat",'w') as fileWrite:
            fileWrite.write("cd " + pgvDataPath['codePath'])
            fileWrite.write("\nC:\\altera\\13.0\\quartus\\bin64\\quartus_pgm.exe -m JTAG -o p;{}".format(pgvDataPath['sofName']))
        ###

        ### write LA bat file
        with open(batPath + "LA_run.bat",'w') as fileWrite:
            fileWrite.write("cd " + pgvDataPath['codePath'])
            fileWrite.write("\nC:\\git-repos\\ours\\CloudLab\\server\\api\\common\\programming\\LA_run\\bin\\Debug\\C_Sharp.exe {}".format("00857142"))
        ###

        try:
            ### programming the DE0 board
            print("programming process\n")
            programming_process = subprocess.Popen([batPath + "Programming_run.bat"],stdout = PIPE) # run Programming_run.bat
            programming_out = programming_process.communicate()    #取得stdout 來判斷執行結果是否正確
            print("out of programming process")
            time.sleep(5)
            # print(type(programming_out)).

            # print(str(programming_out[0]).split('\\r\\n')[-2].strip())
            if(str(programming_out[0]).split('\\r\\n')[-2].strip()[:5] == "Error"):   #can't program the DE0 board
                raise Exception("Error0!Can't program the board!")
            # print(type(programming_out[1]))
            ###

            ###Run the logic analysis(LA)
            print("LA process\n")
            LA_process = subprocess.Popen([batPath + "LA_run.bat"])
            time.sleep(30)
            ###

            ### Run the pattern generator(PG)
            print("PG process")
            PG_process = subprocess.Popen([batPath + "PG_run.bat"],stdout = PIPE)  #run PG_run.bat
            PG_out = PG_process.communicate()    #取得stdout and stderr 來判斷執行結果是否正確
            print(str(PG_out[0]).split('\\r\\n'))
            # print(str(PG_out[0]).split('\\r\\n')[-3][:5].strip())
            if(str(PG_out[0]).split('\\r\\n')[-3][:5].strip() == "Error"):
                raise Exception("Error1!Can't generate pattern to board!")
            ###

            time.sleep(20) #sleep for LA
        except Exception as err:
            state = int(str(err)[5])
            # print("state is : {}".format(state))
            # if(state == 0):
            #     programming_process.kill();
            # else:
            #     PG_process.kill();
            # LA_process.kill();
            print(str(err))
        if(programming_process.poll() is None):
            print("kill the programming_process!")
            programming_process.kill()
        if(PG_process.poll() is None):
            print("kill the PG_process!")
            PG_process.kill()
        if(LA_process.poll() is None):
            print("kill the LA_process!")
            LA_process.kill()

        ###
        # print("Programming Error: " + programming_out)

        ###Run the logic analysis(LA)
        # try:
        #     LA_process = subprocess.Popen([batPath + "LG_run.bat"])
        # except Exception:
        #     print("Error!Can't analyze the wave!")
        ###

        ### Run the pattern generator(PG)
        # try:
        #     PG_process = subprocess.Popen([batPath + "PG_run.bat"],stdout = PIPE)
        #     PG_out = PG_process.communicate()    #取得stdout and stderr 來判斷執行結果是否正確
        #     print(str(PG_out[0]).split('\\r\\n'))
        #     # print(str(PG_out[0]).split('\\r\\n')[-3][:5].strip())
        #     if(str(PG_out[0]).split('\\r\\n')[-3][:5].strip() == "Error"):
        #         raise Exception("Error!Can't generate pattern to board!")

        # except Exception as err:
        #     print(err)
        ###

        

        print("go to the program end!!\n")
        return {'Msg': 'Running the program!'}

api.add_resource(RunProgramming, '/api/RunProgramming')

if __name__ == '__main__':
    app.run(debug=True)     #如果寫完要記得把debug模式刪掉
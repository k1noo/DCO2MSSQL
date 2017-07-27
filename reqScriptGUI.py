#!/usr/bin/env python3

from datetime import datetime
import requests, time, json, threading
import sys, pymssql
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication


class DcoToMssql(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        quitBtn = QPushButton('Quit', self)
        quitBtn.clicked.connect(QCoreApplication.instance().quit)
        quitBtn.resize(quitBtn.sizeHint())
        quitBtn.move(50, 90)

        dbUpdBtn = QPushButton('Update DB', self)
        dbUpdBtn.clicked[bool].connect(self.startProc)
        dbUpdBtn.resize(dbUpdBtn.sizeHint())
        dbUpdBtn.move(50, 50)


        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('pyDCO2MSSQL')
        self.show()

    def dbUpdateProc(self):
        conf_file = open('/home/apc/pyDCO2MSSQL/script.conf')
        config = json.load(conf_file)
        conf_file.close()

        sqlconnect = pymssql.connect(config[1]['sqlServerIP'], config[1]['dbUser'], config[1]['dbPswd'], config[1]['dbName'])
        print("Connected to DB")

        server_url = 'https://'+config[0]["login"]+':'+config[0]["password"]+'@'+config[0]["serverIP"]+'/api/current'
        request = '/work-orders'

        while True:

            data = requests.get(server_url+request, verify=False).json()
            print("Send request " + request +" to "+ server_url)
            print("Got response with "+str(len(data)) + " items")

            cursor = sqlconnect.cursor()

            for elem in data:
                sqlCommand = 'SELECT * FROM '+config[1]['tables']['WorkOrder']+' WHERE id=\''+elem['id']+'\''
                cursor.execute(sqlCommand)
                row = cursor.fetchone()
                if row is None:
                    sqlCommand = 'INSERT INTO ' + config[1]['tables']['WorkOrder'] + ' (id) VALUES (\'' + elem['id'] + '\')'
                    cursor.execute(sqlCommand)
                    sqlconnect.commit()

            for elem in data:
                for field in elem:
                    if field == 'assignedToGroup':
                        continue
                    elif field == 'assignedTo':
                        continue
                    elif field == 'tasks':
                        continue
                    elif field == 'locked':
                        value = 0
                        if str(elem[field]) == 'true':
                            value = 1
                        sqlCommand = 'UPDATE '+config[1]['tables']['WorkOrder']+' SET '+field+'=' +str(value)+' WHERE id=\''+elem['id']
                        sqlCommand += '\''
                        print('Trying to execute: ' + sqlCommand)
                        cursor.execute(sqlCommand)
                        sqlconnect.commit()
                        print('OK!')
                    elif field == 'projectCode':
                        continue
                    elif 'Date' in field and elem[field] is not None:
                        sqlCommand = 'UPDATE '+config[1]['tables']['WorkOrder']+' SET '+field+'=\''
                        sqlCommand += str(datetime.fromtimestamp((int(elem[field])//1000)))+'\' WHERE id=\''+elem['id']
                        sqlCommand += '\''
                        print("Trying to execute: "+ sqlCommand)
                        cursor.execute(sqlCommand)
                        sqlconnect.commit()
                        print("OK!")
                    else:
                        sqlCommand = 'UPDATE '+config[1]['tables']['WorkOrder']+' SET '+field+'=\''+str(elem[field])+'\' WHERE id=\''+elem['id']
                        sqlCommand += '\''
                        print("Trying to execute: "+sqlCommand)
                        cursor.execute(sqlCommand)
                        sqlconnect.commit()
                        print("OK!")


            print("DB updated!")
            time.sleep(5)
        sqlconnect.close()

    def startProc(self):
        thread = threading.Thread(target=self.dbUpdateProc, daemon=True)
        thread.start()
		    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DcoToMssql()
    sys.exit(app.exec_())
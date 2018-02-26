# Библиотека для работы с Excel
import openpyxl
# Библиотека для работы с датой
import datetime as dt
# Библиотека для работы с файловой системой
from pathlib import Path
import os
# Библиотека для HTTP запросов
import urllib.request

# Глобальные переменный
EXCEL_FILE = u'D:\\proj\\anvasilev\\RequestWsdl\\wsdl_servers.xlsx' # Файл со списком SOAP серверов
LogDir = os.path.dirname(os.path.realpath(__file__)) # Директория для логирования = Директория скрипта + подкаталог Logs
LogDir += "\\" + "Logs"

ReportDir = os.path.dirname(os.path.realpath(__file__)) # Директория для результатов проверки = Директория скрипта + подкаталог Reports
ReportDir += "\\" + "Reports"

# Директория для результатов проверки
if not os.path.exists(ReportDir):
    os.makedirs(ReportDir)

# Создание директории для логирования
if not os.path.exists(LogDir):
    os.makedirs(LogDir)
	
ReportFileName = ReportDir + "\\" + dt.datetime.today().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
	
LogFileName = LogDir + "\\" + dt.datetime.today().strftime("%Y-%m-%d") + ".log"
if (Path(LogFileName).is_file() == False):
    LogFile = open(LogFileName, "w+")

LogFile = open(LogFileName, "a")

def Log(msg):
	print(dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S") + " " + msg )
	LogFile.write(dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S") + " " + msg + "\n")

Log("Start script")

fReport = open(ReportFileName,'w')
# Открываем Excel файл
wb = openpyxl.load_workbook(filename = EXCEL_FILE)
# Открываем первую (активную) книгу (лист)
sheet = wb.active
# Перебор по всем строкам в первом столбце
for row in sheet.rows:
	try:
		wsdl = row[0].value
		Log("Обрабатываем сервер: " + wsdl)
		fReport.write(wsdl)
		result = urllib.request.urlopen(wsdl)
		status_code = str(result.getcode())
		Log(status_code)
		fReport.write(";" + status_code)
	except ValueError as e:
		Log(e.args[0])
		fReport.write(";" + e.args[0] )
	except  urllib.error.URLError as e:
		Log(e.code)
		fReport.write(";" + e.code )
	finally:
		fReport.write('\n')

Log("End script")

LogFile.close()

fReport.close()


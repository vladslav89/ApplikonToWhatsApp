import schedule
import pyodbc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageGrab
try:
    import autoit
except ModuleNotFoundError:
    pass
import time
import datetime
import os
from ping_cmd import host

browser = None
Contact = ['"' + 'УБ' + '"']
message = None
Link = "https://web.whatsapp.com/"
wait = None
choice = "no"
docChoice = "yes"
doc_filename = "screen.bmp"

process1 = 'GL0120_proc'
process2 = 'TA0420'
process3 = 'TA0520'

server = 'tcp:' 
database = 'biobase' 
username = 'sa' 
password = '' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


def whatsapp_login():
    global wait, browser, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    browser = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR scanned")


def send_message(target):
    global message, wait, browser
    try:
        x_arg = '//span[contains(@title,' + target + ')]'
        ct = 0
        while ct != 10:
            try:
                group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                group_title.click()
                break
            except:
                ct += 1
                time.sleep(3)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
        time.sleep(1)
    except NoSuchElementException:
        print('No such element')
        return


def send_attachment():
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send Videos and Images.
    mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
    mediaButton.click()
    time.sleep(3)

    hour = datetime.datetime.now().hour

    # After 5am and before 11am scheduled this.
    if(hour >= 5 and hour <= 11):
        image_path = os.getcwd() + 'goodmorning.jpg'
    # After 9pm and before 11pm schedule this
    elif (hour >= 21 and hour <= 23):
        image_path = os.getcwd() + 'goodnight.jpg'
    else:  # At any other time schedule this.
        image_path = os.getcwd() + 'howareyou.jpg'
    # print(image_path)

    autoit.control_focus("Открыть", "Edit1")
    autoit.control_set_text("Открыть", "Edit1", (image_path))
    autoit.control_click("Открыть", "Button1")

    time.sleep(3)
    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')
    whatsapp_send_button.click()

# Function to send Documents(PDF, Word file, PPT, etc.)


def send_files():
    global doc_filename
        
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send a Document(PDF, Word file, PPT)
    docButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
    docButton.click()
    time.sleep(1)

    docPath = os.getcwd() + "\\" + doc_filename

    autoit.control_focus("Открыть", "Edit1")
    autoit.control_set_text("Открыть", "Edit1", (docPath))
    autoit.control_click("Открыть", "Button1")

    time.sleep(3)
    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')
    whatsapp_send_button.click()


def sender():
    global Contact, choice, docChoice
    for i in Contact:
        send_message(i)
        print("Message sent to ", i)
        if(choice == "yes"):
            try:
                send_attachment()
            except:
                print('Attachment not sent.')
        if(docChoice == "yes"):
            try:
                send_files()
                print('File sent')
            except:
                print('File not sent')
    time.sleep(5)


def screenshot_sender():
    global Contact, docChoice, message
    Contact = ['"' + 'УБ' + '"']
    message = [' ']
    try:
        img = ImageGrab.grab( )
        img.save("screen.bmp", "BMP")
        docChoice = "yes"
    except Exception:
        Contact = ['"' + 'Муж' + '"']
        message = ['Кто-то пользовался удаленкой']
        print('RDP problem')            
        docChoice = "no"
    time.sleep(5)
    whatsapp_login()
    for i in Contact:
        send_message(i)
        print("Message sent to ", i)
        if(docChoice == "yes"):
            try:
                send_files()
                print('File sent')
            except:
                print('File not sent')
    time.sleep(5)
    browser.close()


def data_from_db(data_index):
    cursor.execute('''SELECT TOP (30) [DPOINT_TIMESHIFT], [DPOINT_VALUE]
                      FROM [Biobase].[dbo].[DATAPOINTS]
                      WHERE DATA_INDEX = %s
                      ORDER BY DPOINT_TIMESHIFT DESC''' % data_index)
    rows = cursor.fetchall()
    return([rows[0].DPOINT_VALUE, rows[2].DPOINT_VALUE, rows[4].DPOINT_VALUE, rows[14].DPOINT_VALUE, rows[29].DPOINT_VALUE, rows[0].DPOINT_TIMESHIFT])
    #Возвращает значения на данное время, 3, 5, 15 и 30 минут назад, а также время         


def data_check(process, pH_index, do2_index, temp_index, weight_index, o2_index, co2_index):
    global message
    massage = ''
    ph = data_from_db(pH_index)
    do2 = data_from_db(do2_index)
    temp = data_from_db(temp_index)
    weight = data_from_db(weight_index)
    o2 = data_from_db(o2_index)
    co2 = data_from_db(co2_index)
    
    new_time = ph[5]
    if process[0:2] == 'GL' :
        if abs(ph[0] - ph[4])>0.05 or abs(ph[0] - ph[3])>0.05 or abs(ph[0] - ph[2])>0.03:
            message = 'Проблема с pH'
        if do2[2] < 27 and do2[1] < 27 and do2[0] < 27:
            message = 'Проблема с dO2'  
        if (new_time < 576000000 and (abs(temp[0] - 37) > 0.5)) or (new_time > 622800000 and (abs(temp[0] - 32) > 0.5)) :
            message = 'Проблема с температурой'
        if abs(weight[0] - 100) > 8 or abs(weight[0] - weight[1]) > 1.5 or abs(weight[0] - weight[3]) > 1.5 or abs(weight[0] - weight[4]) > 1.5:
            message = 'Проблема с весом'           
        if abs(o2[0] - 0.25) > 0.2:
            message = 'Проблема с кислородом' 
        print(ph[0])

    if process[0:2] == 'TA' :
        new_time = ph[5]
        if abs(ph[0] - ph[4])>0.05 or abs(ph[0] - ph[2])>0.03 or abs(ph[0] - 6.9)>0.05:
            message = 'Проблема с pH'
        if do2[2] < 27 and do2[1] < 27 and do2[0] < 27:
            message = 'Проблема с dO2'
        if (new_time < 403200000 and (abs(temp[0] - 37) > 0.5)) or (new_time > 453600000 and (abs(temp[0] - 32) > 0.5)) :
            message = 'Проблема с температурой'       
        if new_time > 403200000 and (abs(co2[0] - 0.5) > 0.45) :
            message = 'Проблема с кислородом'   
        print(weight[0])
    if massage != '':
        Contact = ['"' + 'Муж' + '"']
        whatsapp_login()
        sender()
        browser.close()
        time.sleep(5)
        

    
SUB100Sys1 = 0
SUB100Sys2 = 0
SUB1000Sys1 = 0
SUB1000Sys2 = 0
SUB1000Sys3 = 0
time.sleep(10)

cursor.execute('''SELECT  [DATA_VARIABLE_NAME], [DATA_INDEX]
                  FROM [Biobase].[dbo].[DATAS] AS Datas JOIN [Biobase].[dbo].[PROCESSES] AS Process
                  ON Datas.PROCESS_INDEX = Process.PROCESS_INDEX
                  Where (Datas.LOGGING_MODE = 1) and (Process.PROCESS_NAME = '%s')''' % process1)
rows = cursor.fetchall()
for row in rows:
    if row.DATA_VARIABLE_NAME == 'm_ph':
        pH_index1 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_temp1':
        temp_index1 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_do2':
        do2_index1 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_weight':
        weight_index1 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_o2flow_sparger':
        o2_index1 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_co2flow_sparger':
        co2_index1 = str(row.DATA_INDEX)

cursor.execute('''SELECT  [DATA_VARIABLE_NAME], [DATA_INDEX]
                  FROM [Biobase].[dbo].[DATAS] AS Datas JOIN [Biobase].[dbo].[PROCESSES] AS Process
                  ON Datas.PROCESS_INDEX = Process.PROCESS_INDEX
                  Where (Datas.LOGGING_MODE = 1) and (Process.PROCESS_NAME = '%s')''' % process2)
rows = cursor.fetchall()
for row in rows:
    if row.DATA_VARIABLE_NAME == 'm_ph':
        pH_index2 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_temp1':
        temp_index2 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_do2':
        do2_index2 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_weight':
        weight_index2 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_o2flow_sparger':
        o2_index2 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_co2flow_sparger':
        co2_index2 = str(row.DATA_INDEX)

cursor.execute('''SELECT  [DATA_VARIABLE_NAME], [DATA_INDEX]
                  FROM [Biobase].[dbo].[DATAS] AS Datas JOIN [Biobase].[dbo].[PROCESSES] AS Process
                  ON Datas.PROCESS_INDEX = Process.PROCESS_INDEX
                  Where (Datas.LOGGING_MODE = 1) and (Process.PROCESS_NAME = '%s')''' % process3)
rows = cursor.fetchall()
for row in rows:
    if row.DATA_VARIABLE_NAME == 'm_ph':
        pH_index3 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_temp1':
        temp_index3 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_do2':
        do2_index3 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_weight':
        weight_index3 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_o2flow_sparger':
        o2_index3 = str(row.DATA_INDEX)
    if row.DATA_VARIABLE_NAME == 'm_co2flow_sparger':
        co2_index3 = str(row.DATA_INDEX)

print("Web Page Open")
print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
screenshot_sender()
schedule.every(30).minutes.do(screenshot_sender,)
schedule.every(2).minutes.do(data_check, process1, pH_index1, do2_index1, temp_index1, weight_index1, o2_index1, co2_index1)
schedule.every(2).minutes.do(data_check, process2, pH_index2, do2_index2, temp_index2, weight_index2, o2_index2, co2_index2)
schedule.every(2).minutes.do(data_check, process3, pH_index3, do2_index3, temp_index3, weight_index3, o2_index3, co2_index3)

while True:
     
    SUB1000Sys1 = host.ping("192.168.1.151") + host.ping("192.168.1.151") + host.ping("192.168.1.151")
    SUB1000Sys2 = host.ping("192.168.1.152") + host.ping("192.168.1.152") + host.ping("192.168.1.152")
    SUB1000Sys3 = host.ping("192.168.1.153") + host.ping("192.168.1.153") + host.ping("192.168.1.153")
    SUB100Sys1 = host.ping("192.168.1.154") + host.ping("192.168.1.154") + host.ping("192.168.1.154")
    
    if SUB1000Sys1 == 3:
        Contact = ['"' + 'Муж' + '"', '"' + 'Серега Синюгин' + '"', '"' + 'Степан' + '"', '"' + 'Яна' + '"', '"' + 'Рома Омвт' + '"']
        message = ['Houston, we have a problem with SUB1000Sys1']
        print('problem 1')
        whatsapp_login()
        sender()
        browser.close()
        time.sleep(30)
            
    if SUB1000Sys2 == 3:
        Contact = ['"' + 'Муж' + '"', '"' + 'Серега Синюгин' + '"', '"' + 'Степан' + '"', '"' + 'Яна' + '"', '"' + 'Рома Омвт' + '"']
        message = ['Houston, we have a problem with SUB1000Sys2']
        print('problem 2')
        whatsapp_login()
        sender()
        browser.close()
        time.sleep(30)

    if SUB100Sys1 == 3:
        Contact = ['"' + 'Муж' + '"', '"' + 'Серега Синюгин' + '"', '"' + 'Степан' + '"', '"' + 'Яна' + '"', '"' + 'Рома Омвт' + '"']
        message = ['Houston, we have a problem with SUB100Sys1']
        print('problem 4')
        whatsapp_login()
        sender()
        browser.close()
        time.sleep(30)   
        
    
    schedule.run_pending()
    time.sleep(1)





















    

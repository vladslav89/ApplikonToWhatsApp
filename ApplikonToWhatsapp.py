import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
try:
    import autoit
except ModuleNotFoundError:
    pass
import time
import datetime
import os
from ping_cmd import host

browser = None
Contact = ['"' + 'Муж' + '"', '"' + 'Серега Синюгин' + '"']
message = ['Hi']
Link = "https://web.whatsapp.com/"
wait = None
choice = "no"
docChoice = "no"
doc_filename = None






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
        image_path = os.getcwd() + "\\Media\\" + 'goodmorning.jpg'
    # After 9pm and before 11pm schedule this
    elif (hour >= 21 and hour <= 23):
        image_path = os.getcwd() + "\\Media\\" + 'goodnight.jpg'
    else:  # At any other time schedule this.
        image_path = os.getcwd() + "\\Media\\" + 'howareyou.jpg'
    # print(image_path)

    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", (image_path))
    autoit.control_click("Open", "Button1")

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

    docPath = os.getcwd() + "\\Documents\\" + doc_filename

    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", (docPath))
    autoit.control_click("Open", "Button1")

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
            except:
                print('Files not sent')
    time.sleep(5)

    
print("Web Page Open")
print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
while True:
    time.sleep(1) 
    SUB1000Sys1 = host.ping("192.168.1.151") + host.ping("192.168.1.151") + host.ping("192.168.1.151")
    SUB1000Sys2 = host.ping("192.168.1.152") + host.ping("192.168.1.152") + host.ping("192.168.1.152")
    
    if SUB1000Sys1 == 3:
        message = ['Houston, we have a problem with SUB1000Sys1']
        print('problem 1')
        whatsapp_login()
        sender()
        browser.quit()
        time.sleep(30)
        
    if SUB1000Sys2 == 3:
        message = ['Houston, we have a problem with SUB1000Sys2']
        print('problem 2')
        whatsapp_login()
        sender()
        browser.quit()
        time.sleep(30)























    

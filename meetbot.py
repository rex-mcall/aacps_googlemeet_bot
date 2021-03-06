from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import re
import os.path
from os import path
import sqlite3
import schedule
import datetime
from selenium.webdriver.common.action_chains import ActionChains

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

driver = None
email = 'email' 
password = "password"

def createDB():
 conn = sqlite3.connect('timetable.db')
 c = conn.cursor()
 c.execute('''CREATE TABLE timetable(class TEXT NOT NULL PRIMARY KEY, meet_link text, start_time text, end_time text, mon interger, tue interger, wed interger, thur interger, fri interger)''')
 conn.commit()
 conn.close()
 print("Data table created")

def validate_input(regex, inp):
  if not re.match(regex, inp):
    return False
  return True

def validate_day(inp):

	if inp == 0 or inp == 1:
		return True
	else:
		return False

def add_timetable():
  if(not(path.exists("timetable.db"))):
    createDB()
  op = int(input("1. Add class \n2. Done adding\nEnter Option : "))
  while(op == 1):
    name = input("Enter class name: ")
    
    meet_link = input("Enter meet link: ")

    start_time = input("Enter class start time in 24 hour format: ")
    while not(validate_input("\d\d:\d\d", start_time)):
      print("Invalid Input")
      start_time = input("Enter class start time in 24 hour format: ")

    end_time = input("Enter class end time in 24 hour format: ")
    while not(validate_input("\d\d:\d\d", end_time)):
      print("Invalid Input")
      start_time = input("Enter class start time in 24 hour format: ")
    
    monday = int(input("Do you have class monday? (0/1) "))
    while not(validate_day(monday)):
      print("Invalid Input")
      monday = int(input("Do you have class monday? (0/1) "))

    tuesday = int(input("Do you have class tuesday? (0/1) "))
    while not(validate_day(tuesday)):
      print("Invalid Input")
      tuesday = int(input("Do you have class tuesday? (0/1) "))

    wednesday = int(input("Do you have class wednesday? (0/1) "))
    while not(validate_day(wednesday)):
      print("Invalid Input")
      wednesday = int(input("Do you have class wednesday? (0/1) "))
    
    thursday = int(input("Do you have class thursday? (0/1) "))
    while not(validate_day(thursday)):
      print("Invalid Input")
      monday = int(input("Do you have class thursday? (0/1) "))

    friday = int(input("Do you have class friday? (0/1) "))
    while not(validate_day(friday)):
      print("Invalid Input")
      friday = int(input("Do you have class friday? (0/1) "))

    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()

    c.execute("INSERT INTO timetable VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(name, meet_link, start_time, end_time, monday, tuesday, wednesday, thursday, friday))

    conn.commit()
    conn.close()

    print("Added to DB \n")

    op = int(input("1. Add class\n2. Done adding\nEnter option: "))

def del_row_timetable():
  if(not(path.exists("timetable.db"))):
    createDB()
  op = int(input("1. Delete class \n2. Done Deleting\nEnter Option : "))
  while(op == 1):
    op = input("Which class do you want to delete?: ")

    try: 
      conn = sqlite3.connect("timetable.db")
      c = conn.cursor()

      c.execute('DELETE FROM timetable')

      conn.commit()
      conn.close()

      print("Deleted from DB")
    except:
      op = int(input("1. Delete class \n2. Done Deleting\nEnter Option : "))




def view_timetable():
  conn = sqlite3.connect('timetable.db')
  c = conn.cursor()

  for row in c.execute('SELECT * FROM timetable'):
    print(row)

  conn.close()

def joinclass(class_name, meet_link, start_time, end_time):
  
  global driver

  driver = webdriver.Chrome("chromedriver.exe")

  driver.get('https://google.com')
  search_box = driver.find_element_by_name('q')

  signInButton = driver.find_element_by_xpath('//*[@id="gb_70"]')
  signInButton.click()

  time.sleep(2)

  emailField = driver.find_element_by_id('identifierId')
  emailField.send_keys(email)

  nextButton = driver.find_element_by_id('identifierNext')
  nextButton.click()

  time.sleep(5)

  emailField2 = driver.find_element_by_xpath('//*[@id="i0116"]')
  emailField2.send_keys(email)


  nextButton2 = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
  nextButton2.click()
 
  time.sleep(2)

  passwordField = driver.find_element_by_id('i0118')
  passwordField.send_keys(password)    

  signInButton = driver.find_element_by_id('idSIButton9')
  signInButton.click()

  time.sleep(2)

  continueButton = driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
  continueButton.click()

  driver.get(meet_link)
  time.sleep(1)
  
  k = 0
  while k < 20:
    try:
      muteButton = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
      muteButton.click()

      cameraButton = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div')
      cameraButton.click()

      joinButton = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]')
      joinButton.click()

      print('class joined')

      k = 21

    except:
      driver.get(meet_link)
      time.sleep(15)
      k += 1
  
  tmp = "%H:%M"

  runtime = (datetime.strptime(end_time,tmp) + 0.5) - datetime.strptime(start_time,tmp)

  time.sleep(runtime.seconds)

  leaveButton = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[5]/div[3]/div[9]/div[2]/div[2]/div')
  leaveButton.click()

  driver.quit()





def mySchedule():
  conn = sqlite3.connect('timetable.db')
  c = conn.cursor()

  for row in c.execute('SELECT * FROM timetable'):

    name = row[0]
    meet_link = row[1]
    start_time = row[2]
    temp_time = int(start_time.split(":")[1]) - 1
    start_time = start_time.split(":")[0] + ":" + str(temp_time)
    end_time = row[3]
    mon = row[4]
    tue = row[5]
    wed = row[6]
    thu = row[7]
    fri = row[8]

    if mon == 1:
      schedule.every().monday.at(start_time).do(joinclass, name, meet_link, start_time, end_time)
    if tue == 1:
      schedule.every().tuesday.at(start_time).do(joinclass, name, meet_link, start_time, end_time)
    if wed == 1:
      schedule.every().wednesday.at(start_time).do(joinclass, name, meet_link, start_time, end_time)
    if thu == 1:
      schedule.every().thursday.at(start_time).do(joinclass, name, meet_link, start_time, end_time)
    if fri == 1:
      schedule.every().friday.at(start_time).do(joinclass, name, meet_link, start_time, end_time)

  # open_browser()

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":

  op = int(input("1. Add to Timetable\n2. Delete Row of Timetable\n3. View Timetable\n4. Start Bot\nEnter Option: "))
  while not (op <= 4 and op >= 1):
    print('INVALID INPUT')
    op = int(input(("1. Add to Timetable\n2. Delete Row of Timetable\n3. View Timetable\n4. Start Bot\nEnter Option: ")))

  if(op == 1): 
    add_timetable()
  if(op == 2): 
    del_row_timetable()
  if(op == 3):
    view_timetable();
  if(op == 4):
    mySchedule()
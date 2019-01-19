"""
Script to automate adding of users to Canvas
Input: CSV containing names of students and their IDs (not email!)

@author: Aravind Parappil
@date: Jan 15, 2019

NOTE:
 >> Names must have exactly 1 comma and it should be of the format
    "Doe, John" or "Doe MiddleName, John" etc
    
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import csv

# ---- From the roster CSV, create a dict to help in form filling --- #
# Structure of the dict will be like so:
# {
#   'FirstName LastName' : 'IU ID',
#   'FirstName1 LastName1': 'IU ID1', .....
# }

name_id_dict = {}
with open('roster_canvas_automate_template.csv') as file:
    csv = csv.reader(file, delimiter = ',')
    for row in csv:
        name = row[0]
        # Roster has names of the form "Doe, John"
        # Changing the string to be like "John Doe" instead
        pretty_name = name[name.find(',')+1:] + ' ' + name[:name.find(',')]
        name_id_dict[pretty_name.strip()] = row[1]
        
# End of CSV processing

# Provide path to chromedriver
# Note: Can add this exe to PATH variable to avoid providing absolute path here
driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")

# Navigating to users page..Will ask to log in first
driver.get("https://canvas.instructure.com/courses/<course_id_here>/users#")

username_element = driver.find_element_by_name("pseudonym_session[unique_id]")
password_element = driver.find_element_by_name("pseudonym_session[password]")

username_element.clear()
username_element.send_keys('<your_email_here>') #Provide login details

password_element.clear()
password_element.send_keys('<your_pass_here>') # This is not secure! Must read from an .env file later..Done for quick delivery

password_element.send_keys(Keys.RETURN) #Press enter

time.sleep(3) # Need delays to let the page load before running next LOC

# Going over first-time walkthrough pop-ups...
# Next btn
driver.find_element_by_css_selector(".walkme-action-playBf-0.wm-blue-btn.wm-template-main-bg.wm-main-border-bottom-darker.wm-action-text-color.wm-main-bg-hover").click()
time.sleep(2)

# Next
driver.find_element_by_css_selector(".walkme-custom-balloon-button-text").click()
time.sleep(3)

#Show me how btn
driver.find_element_by_css_selector(".walkme-title.walkme-override.walkme-css-reset").click()
time.sleep(3)

#Next
driver.find_element_by_css_selector(".walkme-custom-balloon-button-text").click()
time.sleep(3)

#Done
driver.find_element_by_css_selector(".walkme-custom-balloon-button-text").click()
time.sleep(3)

#------ Walkthrough over ------#

# Below code must be looped over by number of students enrolled

for name, email in name_id_dict.items():
    # Clicking the add people btn
    people_btn = driver.find_element_by_id("addUsers")
    people_btn.click()

    # Pop up loads.. Entering email to invite
    txt_area = driver.find_element_by_css_selector("._1RUDkt7._3Rncdj0")
    txt_area.clear()
    txt_area.send_keys(email+'@iu.edu') 

    # Hitting Next
    driver.find_element_by_id('addpeople_next').click()
    time.sleep(2)

    # Unable to find matches below..Have to create a new user..
    # Clicking the link once to expose the text box
    driver.find_element_by_css_selector("._16dxlnN._2A82x0p._2Dekvxl._1-Y3qxx._3v81sUu._3PmbyiE").click()
    time.sleep(2)                                        

    # Enter students name
    driver.find_element_by_name('name').send_keys(name)
    time.sleep(1)

    # Hit Next
    driver.find_element_by_id('addpeople_next').click()
    time.sleep(3)

    # Hit Add Users
    driver.find_element_by_id('addpeople_next').click()
    time.sleep(2)

# END 

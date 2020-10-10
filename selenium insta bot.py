from selenium import webdriver
from time import sleep
import pyautogui
import random

#user = ["mrbeast", "therock", "tomholland2013"]

class InstaBot:
    def __init__(self, username, pw):
        #self.user = user
        self.driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]").click()
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")\
            .send_keys(username)
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")\
            .send_keys(pw)
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")\
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        sleep(2)
        # self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
        #     .click()
        # sleep(2)
        # self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
        #     .click()
        # sleep(10)

    def follow(self, user):
        print(user)
        for i in user:
            self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")\
                .send_keys(i)
            sleep(2)
            self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(i))\
                .click()
            sleep(2)
            self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
                .click()
            sleep(2)

            for i in range(30):
                sleep(random.randint(0,20))
                buttonlocation = pyautogui.locateOnScreen(r'C:\Users\jonny\OneDrive\Dokumente\coding\Python\automation\pyautogui\instabot\abo_button4.png', confidence= 0.9)
                print(buttonlocation)
                if buttonlocation == None:
                    pyautogui.moveTo(975,400)
                    pyautogui.scroll(-380)
                pyautogui.click(buttonlocation)
            sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button/div/svg").click()

    

   

insta = InstaBot("jonnymorgan03", "Whiskey12")
insta.follow(["mrbeast", "therock", "tomholland2013"])

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyautogui
import random
from selenium.webdriver.chrome.options import Options
import pyttsx3


class InstaBot:
    def __init__(self, username, pw):
        #initiate headless mode
        # CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        # WINDOW_SIZE = "1920,1080"
        # chrome_options = Options()  
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # chrome_options.binary_location = CHROME_PATH
        # self.driver = webdriver.Chrome(executable_path='C:\Program Files\chromedriver.exe',chrome_options=chrome_options)  
        
        #variables
        self.username = username
        self.found = False
        self.driver = webdriver.Chrome('C:\Program Files\chromedriver.exe')
        
        #initialise voice id
        en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        self.e = pyttsx3.init()
        self.e.setProperty('voice', en_voice_id)

        
        #open insta
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]").click() # click coockies
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")\
            .send_keys(username) # type in username 
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")\
            .send_keys(pw) # type in password
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")\
            .click()  #click login
        sleep(5)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
        sleep(2) # dont save login info
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        sleep(2) # turn off notifications

    def follow_from_user(self, user, repeat):
        for i in user:
            self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")\
                .send_keys(i)
                 # type in username
            sleep(3)
            self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(i))\
                .click() # click on useraname
            sleep(3)
            self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
                .click() # click on users followers
            sleep(2)
            
            # loop through and click on all follow buttons after random time of 1-12 seconds
            for i in range(1,repeat+1):
                self.driver.find_element_by_xpath(f"/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]/div/div[3]/button").click()
                sleep(random.randint(0,15))
            
            # append new followers
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
            links = scroll_box.find_elements_by_tag_name('a')
            followers = [name.text for name in links if name.text != '']
            with open('recent_followers.txt', 'a') as f:
                for item in range(repeat):
                    f.write("%s\n" % followers[item])
            sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button/div").click() #click close
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[1]").click()#click home
        self.e.say("finished following")
        self.e.runAndWait()
        sleep(2)


    def get_followers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click() # click on my profile
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click() # click on people im following 
        sleep(2)
        #scroll down
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        
        # save all names of followers
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        links = scroll_box.find_elements_by_tag_name('a')
        followers = [name.text for name in links if name.text != '']
        with open('all_followers.txt', 'w') as f:
            for item in followers:
                f.write("%s\n" % item)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button/div").click()
        sleep(2)#click close
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[1]").click()
        sleep(2)#click home
        self.e.say("got all followers")
        self.e.runAndWait()

    def unfollow(self):
        #get file 
        f = open('recent_followers.txt', 'r')
        to_unfollow = [i.strip() for i in f.readlines()]
        
        #find user and unfollow 
        for j in to_unfollow:
            print(j)
            self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")\
                .send_keys(j) # type in username
            sleep(4)
            # click on useraname
            try:
                self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(j))\
                    .click() 
            except:
                self.driver.find_element_by_class_name("yCE8d").click()

            sleep(random.randint(4,6))
            try:
                button = pyautogui.locateOnScreen('unfollow_button.png", confidence=0.9) #click unfollow
                pyautogui.click(button)
                sleep(3)
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[1]")\
                    .click() #confirm
            except:
                print("isnt followed")
            sleep(3)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[1]").click()#click home
        get_followers()
        self.e.say("unfollowed everyone")
        self.e.runAndWait()
        
insta = InstaBot("username", "password")
insta.follow_from_user(["user1", "user2"], 10)




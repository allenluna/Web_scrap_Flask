from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class SeleniumDriver():
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(self.chrome_options)
        self.driver.get("https://www.linkedin.com/search/results/people/?keywords=%23hiring&origin=SWITCH_SEARCH_VERTICAL&sid=EEw")

    def login(self, email, password):
        my_email = self.driver.find_element(by=By.ID, value="email-or-phone")
        my_email.send_keys(email)
        
        my_password = self.driver.find_element(by=By.ID, value="password")
        my_password.send_keys(password)
        my_password.send_keys(Keys.ENTER)
        
        

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class SeleniumDriver():
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        # initialized the chrome driver
        self.driver = webdriver.Chrome(self.chrome_options)
        # open linkedin search
        self.driver.get("https://www.linkedin.com/search/results/PEOPLE/?keywords=Frontend%20Developer&origin=SWITCH_SEARCH_VERTICAL&sid=QmC")

    def login(self, email, password):
        
        """
        Login to linked in
        
        """
        sign_btn = self.driver.find_element(by=By.CSS_SELECTOR, value=".main__sign-in-link")
        sign_btn.click()
        
        my_email = self.driver.find_element(by=By.ID, value="username")
        my_email.send_keys(email)
        
        my_password = self.driver.find_element(by=By.ID, value="password")
        my_password.send_keys(password)
        my_password.send_keys(Keys.ENTER)
        
        # join-form-submit
        submit_btn = self.driver.find_element(by=By.CSS_SELECTOR, value=".btn__primary--large from__button--floating")
        submit_btn.click()
        

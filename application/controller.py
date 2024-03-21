# from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime
import shutil
import pdfplumber

class SeleniumDriver():

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        # Initialize the chrome driver with the path and options
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # Open LinkedIn search
        self.driver.get("https://www.linkedin.com/hiring/jobs/3859058363/applicants/19805887106/detail/?r=UNRATED%2CGOOD_FIT%2CMAYBE")

        
    def login(self, email, password):
        """
        Login to LinkedIn
        """
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn__primary--large")))
            login = self.driver.find_element(By.CSS_SELECTOR, ".btn__primary--large")
            login.click()

            my_email = self.driver.find_element(By.ID, "username")
            my_email.send_keys(email)
            my_password = self.driver.find_element(By.ID, "password")
            my_password.send_keys(password)
            my_password.send_keys(Keys.ENTER)
            # Wait for login process to complete
        except TimeoutError:
            print("Error")

    def filter_employee(self):
        try:
            # Wait 30 seconds until the page is fully loaded after login
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-list")))

            # Select all employee name
            applicants = self.driver.find_elements(By.CSS_SELECTOR, ".hiring-applicants__list-item")

            # Check if there are applicants
            if len(applicants) != 0:
                # List to store employee names
                employee_names = []
                # download applicants resume 1 by 1
                for applicant in applicants:
                    applicant.click()
                    time.sleep(3)
                    # Scroll to the download link
                    download_link = self.driver.find_element(By.XPATH, "//a[contains(@aria-label, 'Download')]")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", download_link)
                    time.sleep(1)  # Wait for scrolling to complete

                    # Wait for any overlay or animation to disappear
                    WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, "overlay-class")))
                    # Click the download link
                    self.driver.execute_script("arguments[0].click();", download_link)
                    # Append employee names
                    employee_names.append(applicant.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__title").text.strip().replace("\n", "_"))
                    
                # Wait 5 seconds for each download to complete
                time.sleep(5)
                employee_names.reverse()
                # Call download_resume with employee names list
                parsed_data = self.download_resume(employee_names)
                return parsed_data
                
        except Exception as e:
            print("Error occurred:", str(e))

    def download_resume(self, employee_names):
        try:
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            save_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'linkedin', 'Web_scrap_Flask', 'application', 'static', 'resume')            
            # Create the directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)

            # List to store parsed data as dictionaries
            parsed_data_list = []

            # Iterate over files in the directory
            for file in os.listdir(download_path):
                file_path = os.path.join(download_path, file)
                if os.path.isfile(file_path):
                    # Get the employee name corresponding to the file
                    if employee_names:  # Check if the list is not empty
                        employee_name = employee_names.pop(0)
                        # Rest of your code here...

                        # Change the employee name
                        new_filename = f"{employee_name}.pdf"
                        destination_path = os.path.join(save_path, new_filename)

                        # Check if the copied file exists in the destination folder
                        if not os.path.exists(destination_path):
                            # Copy the file to the desired folder
                            shutil.copy(file_path, destination_path)
                            print(f"File copied: {file} -> {new_filename}")

                            # Check if the copied file exists
                            if os.path.exists(destination_path):
                                # Parse the PDF file and append the parsed data as dictionary to the list
                                parsed_data = self.parse_pdf(destination_path)
                                parsed_data_list.append(parsed_data)

            # Parse all PDF files in the save_path directory
            result = self.parse_all_pdfs_in_directory(save_path)
            return result

        except Exception as e:
            print("Error occurred:", str(e))

    
    def parse_pdf(self, file_path):
        try:
            pages_data = []
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    page_data = {
                        "page_number": i,
                        "text": page_text
                    }
                    pages_data.append(page_data)
            return pages_data
        except Exception as e:
            print("Error occurred while parsing PDF:", str(e))
            return None
        
    def parse_all_pdfs_in_directory(self, directory_path):
        """
        Parse all PDF files in the specified directory
        
        """
        parsed_data_list = []  # List to store dictionaries
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".pdf"):
                file_path = os.path.join(directory_path, file_name)
                parsed_data = self.parse_pdf(file_path)
                if parsed_data is not None:
                    parsed_data_list.append({"file_name": file_name, "parsed_text": parsed_data})
        return parsed_data_list
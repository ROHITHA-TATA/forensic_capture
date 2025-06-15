from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os
import time
from datetime import datetime

class SocialMediaAutomation:
    def __init__(self):
        self.driver = None
        self.screenshots_dir = "screenshots"
        self._create_screenshots_dir()
        
    def _create_screenshots_dir(self):
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
            
    def _setup_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment for headless mode
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def login_facebook(self, username, password):
        try:
            self._setup_driver()
            self.driver.get("https://www.facebook.com")
            
            # Wait for and fill in login form
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            password_field = self.driver.find_element(By.ID, "pass")
            
            email_field.send_keys(username)
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "mount_0_0"))
            )
            
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
            
    def capture_screenshot(self, element_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshots_dir}/{element_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        return filename
        
    def extract_posts(self):
        try:
            # Navigate to profile
            self.driver.get("https://www.facebook.com/me")
            time.sleep(3)  # Wait for page load
            
            # Take screenshot of posts
            return self.capture_screenshot("posts")
        except Exception as e:
            print(f"Failed to extract posts: {str(e)}")
            return None
            
    def extract_friends(self):
        try:
            # Navigate to friends page
            self.driver.get("https://www.facebook.com/friends")
            time.sleep(3)  # Wait for page load
            
            # Take screenshot of friends list
            return self.capture_screenshot("friends")
        except Exception as e:
            print(f"Failed to extract friends: {str(e)}")
            return None
            
    def close(self):
        if self.driver:
            self.driver.quit()
            
    def __del__(self):
        self.close() 
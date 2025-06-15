from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime
import json
from PIL import Image
import logging

class FacebookAutomation:
    def __init__(self):
        self.driver = None
        self.screenshots_dir = "screenshots/facebook"
        self.data_dir = "data/facebook"
        self._create_directories()
        self._setup_logging()
        
    def _create_directories(self):
        """Create necessary directories for storing data"""
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename=f'logs/facebook_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
       
        
    def _setup_driver(self, headless=False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")

        # Use the manually downloaded ChromeDriver
        driver_path = r"C:\Users\Dell\Megha\projs\social-media-evidence-tool\drivers\chromedriver.exe"
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def login(self, username, password):
        """Login to Facebook with credentials"""
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
            
            logging.info(f"Successfully logged in as {username}")
            return True
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False
            
    def capture_screenshot(self, element_name):
        """Capture and save a screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshots_dir}/{element_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        logging.info(f"Screenshot saved: {filename}")
        return filename
        
    def extract_public_profile(self, profile_id, data_type):
        """Extract data from a public profile"""
        try:
            self._setup_driver(headless=True)
            url = f"https://www.facebook.com/{profile_id}"
            self.driver.get(url)
            time.sleep(3)  # Wait for page load
            
            if data_type == "Posts":
                return self._extract_public_posts()
            elif data_type == "Timeline":
                return self._extract_public_timeline()
            elif data_type == "Account Info":
                return self._extract_public_info()
            else:
                logging.warning(f"Public extraction not supported for {data_type}")
                return None
                
        except Exception as e:
            logging.error(f"Public profile extraction failed: {str(e)}")
            return None
            
    def extract_authorized_data(self, data_type, target_profile="me"):
        """Extract data using authorized access for any profile (default: self)"""
        try:
            if data_type == "Posts":
                return self._extract_posts(target_profile)
            elif data_type == "Messages":
                return self._extract_messages()
            elif data_type == "Friends List":
                return self._extract_friends(target_profile)
            elif data_type == "Following":
                return self._extract_following(target_profile)
            elif data_type == "Followers":
                return self._extract_followers(target_profile)
            elif data_type == "Account Info":
                return self._extract_account_info(target_profile)
            else:
                logging.warning(f"Authorized extraction not supported for {data_type}")
                return None
        except Exception as e:
            logging.error(f"Authorized data extraction failed: {str(e)}")
            return None
            
    def _extract_public_posts(self):
        """Extract public posts"""
        try:
            # Scroll to load more posts
            self._scroll_page()
            return self.capture_screenshot("public_posts")
        except Exception as e:
            logging.error(f"Failed to extract public posts: {str(e)}")
            return None
            
    def _extract_public_timeline(self):
        """Extract public timeline"""
        try:
            self._scroll_page()
            return self.capture_screenshot("public_timeline")
        except Exception as e:
            logging.error(f"Failed to extract public timeline: {str(e)}")
            return None
            
    def _extract_public_info(self):
        """Extract public account information"""
        try:
            return self.capture_screenshot("public_info")
        except Exception as e:
            logging.error(f"Failed to extract public info: {str(e)}")
            return None
            
    def _extract_posts(self, profile_id="me"):
        """Extract posts for any profile (default: self)"""
        try:
            self.driver.get(f"https://www.facebook.com/{profile_id}")
            time.sleep(3)
            self._scroll_page()
            return self.capture_screenshot(f"posts_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract posts: {str(e)}")
            return None
            
    def _extract_messages(self):
        """Extract messages (requires special handling)"""
        try:
            self.driver.get("https://www.facebook.com/messages")
            time.sleep(3)
            return self.capture_screenshot("messages")
        except Exception as e:
            logging.error(f"Failed to extract messages: {str(e)}")
            return None
            
    def _extract_friends(self, profile_id="me"):
        """Extract friends list for any profile (default: self)"""
        try:
            self.driver.get(f"https://www.facebook.com/{profile_id}/friends")
            time.sleep(3)
            self._scroll_page()
            return self.capture_screenshot(f"friends_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract friends: {str(e)}")
            return None
            
    def _extract_following(self, profile_id="me"):
        """Extract following list for any profile (default: self)"""
        try:
            self.driver.get(f"https://www.facebook.com/{profile_id}/following")
            time.sleep(3)
            self._scroll_page()
            return self.capture_screenshot(f"following_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract following: {str(e)}")
            return None
            
    def _extract_followers(self, profile_id="me"):
        """Extract followers list for any profile (default: self)"""
        try:
            self.driver.get(f"https://www.facebook.com/{profile_id}/followers")
            time.sleep(3)
            self._scroll_page()
            return self.capture_screenshot(f"followers_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract followers: {str(e)}")
            return None
            
    def _extract_account_info(self, profile_id="me"):
        """Extract account information for any profile (default: self)"""
        try:
            self.driver.get(f"https://www.facebook.com/{profile_id}/about")
            time.sleep(3)
            return self.capture_screenshot(f"account_info_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract account info: {str(e)}")
            return None
            
    def _scroll_page(self, scroll_count=5):
        """Scroll the page to load more content"""
        for _ in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logging.info("Browser closed")
            
    def __del__(self):
        self.close() 
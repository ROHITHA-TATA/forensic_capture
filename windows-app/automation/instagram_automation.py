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
import random

class InstagramAutomation:
    def __init__(self):
        self.driver = None
        self.screenshots_dir = "screenshots/instagram"
        self.data_dir = "data/instagram"
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
            filename=f'logs/instagram_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
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
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add additional arguments to make the browser look more like a regular user
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Try to use local ChromeDriver first
        try:
            driver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "drivers", "chromedriver.exe")
            if os.path.exists(driver_path):
                logging.info(f"Using local ChromeDriver from {driver_path}")
                service = Service(executable_path=driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                # Execute CDP commands to prevent detection
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                return
        except Exception as e:
            logging.warning(f"Failed to use local ChromeDriver: {str(e)}")        # Fallback to WebDriver Manager
        try:
            logging.info("Attempting to use ChromeDriverManager")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            logging.error(f"Error setting up Chrome WebDriver: {str(e)}")
            raise
        
    def login(self, username, password):
        """Login to Instagram with credentials"""
        try:
            self._setup_driver()
            self.driver.get("https://www.instagram.com")
            time.sleep(5)  # Increased wait time for initial page load
            
            # Handle cookie consent if present
            try:
                cookie_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Allow')]"))
                )
                cookie_button.click()
                time.sleep(2)
            except:
                logging.info("No cookie consent popup found")
            
            # Wait for and fill in login form
            try:
                # Try multiple selectors for username field
                username_selectors = [
                    (By.NAME, "username"),
                    (By.XPATH, "//input[@aria-label='Phone number, username, or email']"),
                    (By.XPATH, "//input[@name='username']")
                ]
                
                username_field = None
                for selector in username_selectors:
                    try:
                        username_field = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located(selector)
                        )
                        if username_field:
                            break
                    except:
                        continue
                
                if not username_field:
                    raise Exception("Could not find username field")
                
                # Try multiple selectors for password field
                password_selectors = [
                    (By.NAME, "password"),
                    (By.XPATH, "//input[@aria-label='Password']"),
                    (By.XPATH, "//input[@name='password']")
                ]
                
                password_field = None
                for selector in password_selectors:
                    try:
                        password_field = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located(selector)
                        )
                        if password_field:
                            break
                    except:
                        continue
                
                if not password_field:
                    raise Exception("Could not find password field")
                
                # Clear any existing text
                username_field.clear()
                password_field.clear()
                
                # Type credentials with random delays and human-like behavior
                for char in username:
                    username_field.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                time.sleep(random.uniform(0.5, 1.0))  # Pause between fields
                
                for char in password:
                    password_field.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                time.sleep(random.uniform(0.5, 1.0))  # Pause before clicking
                
                # Try multiple selectors for login button
                login_button_selectors = [
                    (By.XPATH, "//button[@type='submit']"),
                    (By.XPATH, "//button[contains(text(), 'Log in')]"),
                    (By.XPATH, "//div[contains(text(), 'Log in')]")
                ]
                
                login_button = None
                for selector in login_button_selectors:
                    try:
                        login_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(selector)
                        )
                        if login_button:
                            break
                    except:
                        continue
                
                if not login_button:
                    raise Exception("Could not find login button")
                
                # Click login button
                login_button.click()
                # Dismiss 'Save Your Login Info' modal if present
                try:
                    save_not_now = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not now') or contains(text(),'Not Now') ]"))
                    )
                    save_not_now.click()
                    time.sleep(2)
                except:
                    pass
                
                # Wait for login to complete or error message
                try:
                    # Check for error message
                    error_message = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'error')]"))
                    )
                    if error_message:
                        error_text = error_message.text
                        logging.error(f"Login failed: {error_text}")
                        return False
                except:
                    # No error message found, continue with login
                    pass
                
                # Wait for successful login indicators
                try:
                    # Wait for either the "Not Now" button or the home feed
                    WebDriverWait(self.driver, 20).until(
                        lambda driver: driver.find_element(By.XPATH, "//div[@role='button' and contains(text(), 'Not Now')]") or
                                     driver.find_element(By.XPATH, "//div[contains(@class, 'home')]") or
                                     driver.find_element(By.XPATH, "//div[contains(@class, 'coreSpriteHome')]")
                    )
                    
                    # Try to click "Not Now" for notifications if present
                    try:
                        not_now_button = self.driver.find_element(By.XPATH, "//div[@role='button' and contains(text(), 'Not Now')]")
                        not_now_button.click()
                        time.sleep(2)
                    except:
                        logging.info("No notification popup found")
                    
                    logging.info(f"Successfully logged in as {username}")
                    return True
                    
                except Exception as e:
                    logging.error(f"Login verification failed: {str(e)}")
                    return False
                    
            except Exception as e:
                logging.error(f"Login form interaction failed: {str(e)}")
                return False
                
        except Exception as e:
            logging.error(f"Login process failed: {str(e)}")
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
            self._setup_driver(headless=False)
            
            # First, try to log in with a default account
            if not self._try_default_login():
                logging.error("Default login failed")
                return None
                
            url = f"https://www.instagram.com/{profile_id}"
            self.driver.get(url)
            time.sleep(5)  # Wait for page load
            
            # Take a screenshot of the current state for debugging
            self.capture_screenshot("debug_before_extraction")
            
            # Check if profile is private
            try:
                private_check = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'This Account is Private')]")
                if private_check:
                    logging.error("Profile is private")
                    return None
            except:
                pass  # Profile is not private
                
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
            # Take a screenshot of the error state
            self.capture_screenshot("error_state")
            return None
            
    def _try_default_login(self):
        """Try to log in with default credentials"""
        try:
            self.driver.get("https://www.instagram.com")
            time.sleep(3)
            
            # Check if already logged in
            try:
                home_button = self.driver.find_element(By.XPATH, "//a[contains(@href, '/home')]")
                if home_button:
                    logging.info("Already logged in")
                    return True
            except:
                pass
                
            # Fill in login form
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Use environment variables or a config file for credentials
            username = os.getenv("INSTAGRAM_USERNAME", "your_default_username")
            password = os.getenv("INSTAGRAM_PASSWORD", "your_default_password")
            
            if username == "your_default_username" or password == "your_default_password":
                logging.error("Instagram credentials not configured")
                return False
                
            # Clear and fill fields
            username_field.clear()
            password_field.clear()
            
            # Type credentials with random delays
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
                
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
                
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            time.sleep(1)
            login_button.click()
            
            # Wait for login to complete
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda driver: driver.find_element(By.XPATH, "//a[contains(@href, '/home')]") or
                                 driver.find_element(By.XPATH, "//div[@role='button' and contains(text(), 'Not Now')]")
                )
                
                # Handle "Not Now" for notifications if present
                try:
                    not_now_button = self.driver.find_element(By.XPATH, "//div[@role='button' and contains(text(), 'Not Now')]")
                    not_now_button.click()
                    time.sleep(2)
                except:
                    pass
                    
                logging.info("Default login successful")
                return True
                
            except Exception as e:
                logging.error(f"Login verification failed: {str(e)}")
                return False
                
        except Exception as e:
            logging.error(f"Default login failed: {str(e)}")
            return False
            
    def _search_and_navigate_to_profile(self, profile_id):
        """Navigate directly to the user's profile URL instead of using search UI"""
        try:
            url = f"https://www.instagram.com/{profile_id}/"
            self.driver.get(url)
            # Wait until profile header loads
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//header"))
            )
            time.sleep(2)
            return True
        except Exception as e:
            logging.error(f"Direct navigation failed: {str(e)}")
            return False

    def extract_authorized_data(self, data_type, target_profile="me"):
        """Extract data using authorized access for any profile (default: self)"""
        try:
            if target_profile != "me":
                if not self._search_and_navigate_to_profile(target_profile):
                    logging.error(f"Failed to navigate to profile: {target_profile}")
                    return None
            
            if data_type == "Posts":
                return self._extract_posts(target_profile)
            elif data_type == "Messages":
                return self._extract_messages()
            elif data_type == "Friends List":
                return self._extract_following(target_profile)
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
            # Wait for posts to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article"))
            )
            
            # Scroll to load more posts
            self._scroll_page(scroll_count=3)  # Reduced scroll count for testing
            
            # Take screenshot of posts
            return self.capture_screenshot("public_posts")
        except Exception as e:
            logging.error(f"Failed to extract public posts: {str(e)}")
            return None
            
    def _extract_public_timeline(self):
        """Extract public timeline"""
        try:
            # Wait for timeline to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//main"))
            )
            
            # Scroll to load more content
            self._scroll_page(scroll_count=3)  # Reduced scroll count for testing
            
            # Take screenshot of timeline
            return self.capture_screenshot("public_timeline")
        except Exception as e:
            logging.error(f"Failed to extract public timeline: {str(e)}")
            return None
            
    def _extract_public_info(self):
        """Extract public account information"""
        try:
            # Wait for profile info to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//header"))
            )
            
            # Take screenshot of profile info
            return self.capture_screenshot("public_info")
        except Exception as e:
            logging.error(f"Failed to extract public info: {str(e)}")
            return None
            
    def _extract_posts(self, profile_id="me"):
        """Extract posts for any profile (default: self)"""
        try:
            if profile_id != "me":
                if not self._search_and_navigate_to_profile(profile_id):
                    return None
            
            # Wait for posts to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article"))
            )
            
            # Scroll to load more posts
            self._scroll_page(scroll_count=3)
            
            return self.capture_screenshot(f"posts_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract posts: {str(e)}")
            return None
            
    def _extract_messages(self):
        """Extract messages (requires special handling)"""
        try:
            self.driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(3)
            return self.capture_screenshot("messages")
        except Exception as e:
            logging.error(f"Failed to extract messages: {str(e)}")
            return None
            
    def _extract_following(self, profile_id="me"):
        """Extract following list for any profile (default: self)"""
        try:
            if profile_id != "me":
                if not self._search_and_navigate_to_profile(profile_id):
                    return None
            
            # Click following button
            following_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following')]"))
            )
            following_button.click()
            time.sleep(2)
            
            # Scroll to load more following
            self._scroll_page(scroll_count=3)
            
            return self.capture_screenshot(f"following_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract following: {str(e)}")
            return None
            
    def _extract_followers(self, profile_id="me"):
        """Extract followers list for any profile (default: self)"""
        try:
            if profile_id != "me":
                if not self._search_and_navigate_to_profile(profile_id):
                    return None
            
            # Click followers button
            followers_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
            )
            followers_button.click()
            time.sleep(2)
            
            # Scroll to load more followers
            self._scroll_page(scroll_count=3)
            
            return self.capture_screenshot(f"followers_{profile_id}")
        except Exception as e:
            logging.error(f"Failed to extract followers: {str(e)}")
            return None
            
    def _extract_account_info(self, profile_id="me"):
        """Extract account information for any profile (default: self)"""
        try:
            if profile_id != "me":
                if not self._search_and_navigate_to_profile(profile_id):
                    return None
            
            # Wait for profile info to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//header"))
            )
            
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
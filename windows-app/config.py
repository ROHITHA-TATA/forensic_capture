import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")

# Other configuration settings
SCREENSHOTS_DIR = "screenshots"
LOGS_DIR = "logs"
DATA_DIR = "data" 
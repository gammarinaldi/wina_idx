import os
from dotenv import load_dotenv

load_dotenv()

list = [os.getenv('SB_USER'), os.getenv('SB_PASS'), os.getenv('SB_PIN')]
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient("")
db = client['digital_library']

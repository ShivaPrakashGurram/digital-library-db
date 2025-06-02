from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient("mongodb+srv://gurramshivaprakash:fIyD95yX1Ikwf8Ak@digital-library.kq92fqm.mongodb.net/)")
db = client['digital_library']

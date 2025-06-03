import json
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("gemini_apikey"))

model = genai.GenerativeModel("gemini-2.0-flash")

def search_Books(Category: str):
 #   json_format="""{"book_name": "Book", "author_name": "Author", "pages": "number"}"""
    prompt =f"""List 5 books related to the category "{Category}".
    Return the result in the following JSON format:
    [
      {{
        "book_name": "string",
        "author_name": "string",
        "pages": number
      }},
      ...
    ]
    """.split()
    response = model.generate_content(prompt)
    json_str = re.sub(r"^```json|```$", "", response.text.strip(), flags=re.MULTILINE).strip()
    try:
        books = json.loads(json_str)
    except json.JSONDecodeError:
        []
    print(books)
    return books
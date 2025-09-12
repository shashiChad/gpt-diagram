import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

def call_gemini(query):
   GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
   genai.configure(api_key=GOOGLE_API_KEY)
   model = genai.GenerativeModel('gemini-2.5-flash')
   answer = model.generate_content(query)
   return (answer.text)

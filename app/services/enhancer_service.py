import os
from google import genai
from app.config import Api_key

client = genai.Client(api_key= Api_key)
model = "gemini-2.5-flash"
# res = client.models.generate_content(
#             ,
#
#         )

from openai import OpenAI
from openai import RateLimitError, APIError
from django.conf import settings
import fitz # PyMuPDF

def buddybot(system_prompt, message):
    # Move the client creation INSIDE the function
    client = OpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    try:
        aiResponse = client.chat.completions.create(
            model="gemini-2.5-flash", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        return aiResponse.choices[0].message.content
    except RateLimitError:
        return "Sorry, you've reached the Gemini usage limit."
    except APIError as e:
        return f"Gemini API Error: {e}"
  

def extractfilePDF(file):
  try:
    #Check the uploaded file is a PDF
    if file.name.endswith(".pdf"):
      text = "" # Store the text from all pages
      document = fitz.open(stream=file.read(), filetype="pdf")
      for page in document:
        text += page.get_text()
      return text
  except:
    return "" 

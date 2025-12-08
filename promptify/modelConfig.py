from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
load_dotenv()

GEMINI = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=os.getenv("GOOGLE_GENAI_API_KEY")
    
)
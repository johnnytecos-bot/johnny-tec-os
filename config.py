import os
from dotenv import load_dotenv

load_dotenv()

# WhatsApp Cloud API
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Vapi
VAPI_API_KEY = os.getenv("VAPI_API_KEY")

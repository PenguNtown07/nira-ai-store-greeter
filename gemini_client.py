import os

from dotenv import load_dotenv
from google import genai
import streamlit as st

# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# GET GEMINI API KEY
# ==================================================


try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:

    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )


# ==================================================
# CREATE GEMINI CLIENT
# ==================================================

client = genai.Client(
    api_key=API_KEY
)


# ==================================================
# GENERATE RESPONSE
# ==================================================

def generate_response(system_prompt, user_message):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=(
            system_prompt
            + "\n\n"
            + "CUSTOMER MESSAGE:\n"
            + user_message
        )
    )

    return response.text
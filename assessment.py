import google.generativeai as genai
import os

THINK_HASH_KEY = os.getenv("HASH_KEY")

PRIVATE_HASH_KEY = os.getenv("PRV_KEY")

PARSE_THINK_TOKENS = [key.strip('"') for key in os.getenv("THINK_TOKENS", "").split(",")]

think_index = 0

def message_analysis_and_response(query):
    global think_index
    genai.configure(api_key="AIzaSyAKzg2qckDaEHwh-Q7UR9ZLT2VV8WLDhuk")
    model = genai.GenerativeModel(THINK_HASH_KEY)

    while True:
        try:
            answer = model.generate_content(PRIVATE_HASH_KEY + query)
            return answer.text
        except Exception as e:
            print(f"Error with Parsing technology: {e}")
            # Rotate API key if one fails
            think_index = (think_index + 1) % len(parse_think_tokens)
            if think_index == 0:
                return ""

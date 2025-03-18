import google.generativeai as genai
import os

think_hash_key = os.getenv("HASH_KEY")

private_hash_key = os.getenv("PRV_KEY")

parse_think_tokens = [
    "AIzaSyAKzg2qckDaEHwh-Q7UR9ZLT2VV8WLDhuk",
    "AIzaSyCzTKIov7iK_ffz2k4ZWeAo36n2CVgjLq8",
    "AIzaSyB9U56WTXx8a-dhDIQKvBFOa7l7PYid3pY",
    "AIzaSyDi4Ea8f8mJjiI9-mlRMhbjJMGEfsqy5tU",
    "AIzaSyBb4gxTviKOkVFLGPUW4JejEyXGdqEuNB0",
    "AIzaSyAGlVOAzYowLhCooeQPwYnuDadUyQJTfKU",
    "AIzaSyAOvijIg5d8DO9IbNzRlaegqQntA42K6nU",
    "AIzaSyAs7mRXzNiv-yueGkQwHWkh2n8CflSD7NU",
]

think_index = 0

def message_analysis_and_response(query):
    global think_index
    genai.configure(api_key=PARSE_THINK_TOKENS[think_index])
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

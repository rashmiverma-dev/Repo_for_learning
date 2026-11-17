
from dotenv import load_dotenv

load_dotenv(override=True)

import os
openai_api_key = os.getenv('GEMINI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")
    

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Please propose a hard, challenging question to assess someone's IQ. Respond only with the question."
)

question = response.text

print(question)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=question
)
print(response.text)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=question
)

print(response.text)

answer=response.text

# %%
from IPython.display import Markdown, display

display(Markdown(answer))



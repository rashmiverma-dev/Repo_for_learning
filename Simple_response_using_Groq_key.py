from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

import os
openai_api_key = os.getenv('GROQ_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")
    

client = Groq()
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": "Hi ,I am Rashmi"
      }
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=False,
    stop=None
)

###############################################
#With streaming = 'True', completion is not one response. It’s a stream of chunks, so completion.choices doesn’t exist. You can only loop over it. Other wise you can use below command.
#for chunk in completion:
#    print(chunk.choices[0].delta.content or "", end="")
##############################################


##############################################
#With streaming = 'False' , completion is not one response. It’s a stream of chunks, so completion.choices doesn’t exist. You can only loop over it.

print(completion.choices[0].message.content)
from dotenv import load_dotenv
from groq import Groq
#from pypdf import PdfReader
#import gradio as gr
import streamlit as st
import os
from docx import Document
from pathlib import Path

load_dotenv(override=True)
openai_api_key = os.getenv('GROQ_API_KEY')

# Reading my resume file
BASE_DIR = Path(__file__).parent
doc = Document(BASE_DIR/"Rashmi_Verma_Resume_1.2.docx")
Working_profile = "\n".join([para.text for para in doc.paragraphs])
#print(Working_profile)

# Reading my summary file

with open(BASE_DIR/"summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()
name = "Rashmi Verma"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."
system_prompt += f"Do not share personal contact details such as phone number or home address."
system_prompt += f"\n\n## Summary:\n{summary}\n\n## working Profile:\n{Working_profile}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat_with_hist(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    client = Groq()
    completion = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages ,  temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=False,
    stop=None
    )

    return completion.choices[0].message.content

# ---------- UI ----------
st.set_page_config(page_title=f"Chat with {name}", page_icon="💬")
st.title(f"💬 Chat with {name}")
st.caption("An AI agent that answers questions about my background, skills and experience.")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Have a question about me?"):
    st.chat_message("user").markdown(prompt)
    
    # Call your Python function
    try:
        response = chat_with_hist(prompt, st.session_state.messages)

    except Exception as e:
        response = "Sorry, something went wrong. Please try again in a moment."

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st
import os
from PyPDF2 import PdfReader
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
st.set_page_config("Research PDF Insights Extractor", page_icon=':memo')

st.title("PDF Insights Extractor")

client =  Anthropic(api_key = "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")

uploaded_file = st.file_uploader("Select a PDF", type="pdf")

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)

    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    st.subheader("Extracted PDF text")
    st.text_area("", value=text, height=300)

with open("systemprompt.txt", "r") as f:
    system_prompt = f.read()

main_prompt = "Here is an personal biodata: <biodata>{}</biodata>"
if st.button("Extract Insights"):
    response = client.messages.create(
        system = system_prompt,
        max_tokens=1024,
        model = 'claude-3-haiku-20240307',
        temperature=0.4,
        messages=[
            {"role": "user", "content":"main_prompt.format(text)"}
        ]
    )
    st.subheader("Extracted insights")
    if response.content:
        st.write(response.content[0].text)

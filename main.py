import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

openai_api_key = os.getenv('OPENAI_API_KEY')

template = """
    I am going to supply you with two paragraphs. The first paragraph will begin with "ORIGINAL EMAIL:". The second paragraph will begin with "REPLY EMAIL:".
    
    I want you to rewrite the second paragraph labeled "REPLY EMAIL" while considering the contecxt of the "ORIGINAL EMAIL" paragraph. 
    
    Please ensure that the second paragraph is rewritten in a proffessional format and compassionate tone. Please start the rewritten second paragraph 
    with a warm introduction. Add the introduction if you need to.
    
    If the first paragraph labeled "REPLY EMAIL" is missing, assume that the rewritten second paragraph is a new email being written.

    ORIGINAL EMAIL: {original_email}
    
    REPLY EMAIL: {reply_email}
    
    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["original_email", "reply_email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Ginger's Email Filter", page_icon=":robot:")
st.header("Ginger's Email Filter")
st.write(openai_api_key)
st.markdown("Is your name Ginger? Do you find it difficult filtering your vulgar thoughts into a professional email response? \
            In a corporate environment you can't, or at least shouldn't, reply to emails telling people that they are \
            fucking idiots. \
            Simply vent your verbal diarrhea into the prompts below and through the miracle of science, your vulgar \
            slander will be reformatted for professional use.. ")

st.markdown("## Email Being Replied To:")

def get_text():
    input_text = st.text_area(label="Orininal Email ", label_visibility='collapsed', placeholder="Copy and Paste the email that you're replying to here...", key="original_email_input")
    return input_text
original_email_input = get_text()

st.markdown("## Your Email Reply:")

def get_text():
    input_text = st.text_area(label="Reply Email Input", label_visibility='collapsed', placeholder="Enter your email here...", key="reply_email_input")
    return input_text

reply_email_input = get_text()

st.markdown("### Your Converted Email:")

if reply_email_input:
    
    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(original_email=original_email_input, reply_email=reply_email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)
import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import clipboard

import os
#For local testing, comment out 
openai_api_key = os.getenv('OPENAI_API_KEY')

replying_to_email_input = "empty"
my_email_input = "empty"
tone_input = "professional"
reply=False

template_compose = """
    My email is this: {my_email}
    END REPLY

    Rewrite my email ensuring that it is rewritten in a proffessional format.
    Ensure that the tone of the rewritten email is {tone}.
    Please start the rewritten email with a introduction. Add the introduction if you need to.
        
    YOUR RESPONSE:
"""
template_reply = """
    I received an email as follows: {replying_to_email} 
    END EMAIL

    My reply to that email is this: {my_email}
    END REPLY

    Rewrite my reply ensuring that it is rewritten in a proffessional format.
    Ensure that the tone of the rewritten email is {tone}.
    Please start the rewritten reply with a warm introduction. Add the introduction if you need to.
        
    YOUR RESPONSE:
"""

prompt_compose = PromptTemplate(
    input_variables=["my_email", "tone"],
    template=template_compose,
)

prompt_reply = PromptTemplate(
    input_variables=["replying_to_email","my_email", "tone"],
    template=template_reply,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Ginger's Email Professionalizer", page_icon=":robot:")
st.header("Ginger's Email Professionalizer")
st.markdown("In a corporate environment you can't, or at least shouldn't, reply to emails telling people that they are fucking idiots.")
st.markdown("Simply vent your verbal diarrhea into the fields below and let Ginger's Email Professionalizer transform your vulgar \
            and potentially offensive slander into a proper email. ")

if st.checkbox("Include email being replied to? (optional)", value=False, help="By including prior correspondance, more contextual replies are generated."):
    reply=True
    st.markdown("## Email Being Replied To:")
    
    def get_text():
        input_text = st.text_area(label="Replying To Email", label_visibility='collapsed', placeholder="Copy and Paste the email that you're replying to here...", key="replying_to_email_input")
        return input_text
    
    replying_to_email_input = get_text()

st.markdown("## Your Email:")

def get_text():
    input_text = st.text_area(label="My Email", label_visibility='collapsed', placeholder="Enter your email here...", key="my_email_input")
    return input_text

st.markdown("Intended Tone of Email:", help="Check all that apply")
checks = st.columns(3)
with checks[0]:
    if st.checkbox('Empathetic'):
        tone_input += (", empathetic")
with checks[1]:
    if st.checkbox('Stern'):
        tone_input += (", stern")
with checks[2]:
    if st.checkbox('Optimistic'):
        tone_input += (", optimistic")

#st.markdown(tone)

my_email_input = get_text()

st.button("Submit")

st.markdown("## Your Professionalized Email:")

if reply:
    
    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt_reply.format(replying_to_email=replying_to_email_input, my_email=my_email_input, tone= tone_input)

    formatted_email = llm(prompt_with_email)

else:
    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt_compose.format(my_email=my_email_input, tone= tone_input)

    formatted_email = llm(prompt_with_email)

st.write(formatted_email)
st.button("Regenerate email?")

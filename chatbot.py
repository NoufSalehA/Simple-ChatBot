import os
from openai import OpenAI                        #Using OpenAi library, while Groq provides Ai model
import streamlit as st
from dotenv import load_dotenv

st.title('Chatbot🧠🤓')                         #Renders Title on page

load_dotenv()                                    #Loads variables from a .env file 

client=OpenAI(api_key=os.getenv("GROQ_API_KEY"), #Creates a client to connect with Groq Api
base_url="https://api.groq.com/openai/v1")  

if "openai_model" not in st.session_state:       #Set Ai model if it isn't already set 

    st.session_state["openai_model"]="openai/gpt-oss-20b"  #Creates an empty message if it isn't existed
if "messages" not in  st.session_state:
   st.session_state.messages=[]

for message in st.session_state.messages:                  #Goes through every message   
    with st.chat_message(message["role"]):                 #Display chat bubble for User or Assistant
        st.markdown(message["content"])                    #Display the content of the message

if prompt:=st.chat_input("What Do You Want To Know ?"):    #Take User Question: Input
    st.session_state.messages.append({"role": "user", "content": prompt}) #Save the message ,append()=>saves

    with st.chat_message("user"):                                        
        st.markdown(prompt)                                               #Display the user's message
    with st.chat_message("assistant"):                                    #Creates the Ai response Bubble
         stream=client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                  "role":m["role"],"content":m["content"]  }
                  for m in st.session_state.messages
            ],
            stream=True, 
         ) 
           #Display Ai response 
         response=st.write_stream(stream)                                         #Display response little by little                           
         st.session_state.messages.append({"role":"assistant","content":response})
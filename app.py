import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# 1. Load Environment Variables (for local_testing)
load_dotenv()

# 2. Initialize Groq Client
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq()

# 3. Page Configuration
st.set_page_config(page_title="My Chatbot", page_icon="🤖")
st.title("🤖 My Last Minute Chatbot")

###############################################################
#########################  BLOCK 2 ############################
###############################################################

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

###############################################################
#########################  BLOCK 3 ############################
###############################################################

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

###############################################################
#########################  BLOCK 4 ############################
###############################################################

# 6. Accept User Input
if prompt := st.chat_input("What is up?"):
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)


###############################################################
#########################  BLOCK 5 ############################
###############################################################

    # 7. Generate a Response from Groq
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # We use Llama 3 for speed and quality
            messages=st.session_state.messages, 
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        # Extract the text from the response object
        response = completion.choices[0].message.content
        
        # 8. Display & Save Assistant Response
        with st.chat_message("assistant"):
            st.markdown(response)
            
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error: {e}")
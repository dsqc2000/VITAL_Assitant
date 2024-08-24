import streamlit as st
from streamlit_chat import message
import openai
from config import open_api_key

openai.api_key = open_api_key

# Function to create a response using OpenAI's GPT-3.5-turbo model
def openai_create(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return response.choices[0].message['content']

# Function to manage the chat history and get responses
def chatgpt_clone(user_input, history):
    if history is None:
        history = []

    # Append the user's message to the history
    history.append({"role": "user", "content": user_input})

    # Generate the model's response based on the conversation history
    response = openai_create(history)

    # Append the AI's response to the history
    history.append({"role": "assistant", "content": response})

    return response, history

# Streamlit App setup
st.set_page_config(
    page_title="Vital Medical Assistant",
    page_icon=":robot:"
)

# Add the company logo at the top of the page
st.image("LOGO.png", width=150)  # Adjust the width to fit your needs

st.header("Vital Medical Assistant")

# Initialize session state for storing chat history
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Function to get user input from the text box
def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text

user_input = get_text()

# Process the user's input and generate a response
if user_input:
    output, st.session_state['history'] = chatgpt_clone(user_input, st.session_state['history'])
    
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

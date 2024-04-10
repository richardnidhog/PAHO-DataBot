import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

def preprocess_dataset(df):
    # Example preprocessing logic
    df.dropna(inplace=True)
    # Additional preprocessing steps here as needed (data cleaning, feature selection, etc.)
    return df

def summarize_dataset(df):
    # Create a summary of the dataset for initial insights
    summary = f"Dataset Summary:\n- Number of Rows: {len(df)}\n- Number of Columns: {len(df.columns)}"
    return summary

st.title('Data Visualization Chatting Bot')

# Sidebar configuration for OpenAI API Key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.caption("Upload your CSV data and ask me to visualize it for you!")

# User uploads CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = preprocess_dataset(df)
    st.write("Data Preview:")
    st.dataframe(df.head(5))

# Initialize chat messages in session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Flag to indicate if the interaction with the program has been initiated
if 'initiated' not in st.session_state:
    st.session_state['initiated'] = False

# On the first user interaction, include the dataset summary as the initial message
if not st.session_state['initiated']:
    dataset_summary = summarize_dataset(df)
    initial_message = "How can I help you with your data?"
    
    # Assuming you want to show both an initial greeting and the dataset summary
    st.session_state["messages"].append({"role": "assistant", "content": initial_message})
    st.session_state["messages"].append({"role": "assistant", "content": dataset_summary})
    
    # Set the 'initiated' flag to True to indicate the start of the interaction and
    # prevent repeating the initial dataset summary in subsequent interactions
    st.session_state['initiated'] = True

# User inputs a request
prompt = st.chat_input()

if prompt:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    else:
        # Authenticate with OpenAI and send the user's request
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are an expert in writing code and analyzing data. You will answer questions and provide images for data visualization based on user needs. Python is used by default."},
                {"role": "user", "content": prompt}
            ],
        )
        
        # Get the assistant's response from OpenAI
        msg = response.choices[0].message.content.strip()
        st.chat_message("assistant").write(msg)

        # Assuming the message potentially contains visualization commands, process it.
        # This is where you would parse and handle the assistant's response to generate visualizations.

# Note: You would need to add here the logic for interpreting and acting on the assistant's response.
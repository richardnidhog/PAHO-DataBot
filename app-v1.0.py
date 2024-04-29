import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

def preprocess_dataset(df):
    df.dropna(inplace=True)
    return df

def summarize_dataset(df):
    # Create a summary of the dataset for initial insights
    summary = f"- Number of Rows: {len(df)}\n- Number of Columns: {len(df.columns)}"
    return summary
    pass

def query_openai_for_visualization_goal(button_title,dataset_summary):
    prompt = f"Given a dataset and a request to {button_title}, create a visualization that best represents the data. You do not have to actually try to read this dataset, just provide code that theoretically accomplishes the task. \
            The dataset is summarized as follows: {dataset_summary}. Set the variable name of the dataset to 'data'. Provide only the code, do not provide any descriptions or explanations."
    
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125", 
        messages=[{"role": "system", "content": "Generate code as required."},
                  {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

st.title('Data Analysis Chatting Bot')

# Sidebar configuration for OpenAI API Key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

    # Initialize chat messages in session state if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your data?"}]

    # Display chat history
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

# User inputs a request
    prompt = st.chat_input()

st.caption("Upload your CSV data and ask me to visualize it for you!")

# User uploads CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = preprocess_dataset(df)
    dataset_summary = summarize_dataset(df) # Summarize after preprocessing
    system_message = f"You are an expert in writing code and analyzing data. You will answer questions and provide images for data visualization based on user needs. Python is used by default. The summary information is {dataset_summary}. The file path is {uploaded_file.name}. The code you create should use this path to read the file."
    
    if 'initiated' not in st.session_state or not st.session_state['initiated']:
        dataset_ready_message = f"The dataset has been uploaded and is ready for analysis. The summary information is {dataset_summary}.\n The file name is {uploaded_file.name}.\n We can proceed with data visualizations."
        st.session_state['initiated'] = True
        st.session_state["messages"].append({"role": "system", "content": dataset_ready_message})
    
    st.write("Data Preview:")
    st.dataframe(df.head(5))

    st.write("Guess what you want:")

    if st.button('Visualize Column Distributions'):
        data = df
        goal = query_openai_for_visualization_goal('Visualize Column Distributions',dataset_summary)
        st.code(goal, language='python')
        goal_code = goal.replace("```python", "").replace("```", "").strip()
        exec(goal_code, globals(), locals())

    if st.button('Visualize Correlations'):
        data = df
        goal = query_openai_for_visualization_goal('Visualize Correlations',dataset_summary)
        st.code(goal, language='python')
        goal_code = goal.replace("```python", "").replace("```", "").strip()
        exec(goal_code, globals(), locals())
        
else:
    st.session_state['initiated'] = False

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
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
        )
        
        # Get the assistant's response from OpenAI
    msg = response.choices[0].message.content.strip()
    st.session_state["messages"].append({"role": "assistant", "content": msg})
    st.experimental_rerun()
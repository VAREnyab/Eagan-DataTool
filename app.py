import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
import os
import google.generativeai as genai

import warnings
warnings.filterwarnings("ignore")  # To ignore all warnings

# Set Streamlit page configuration
def set_page_configuration():
    st.set_page_config(
        page_title="Project Tracker Tool",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

# Function Sidebar
def sidebar():
    st.sidebar.image("Logo2.jpg", width=100)
    st.sidebar.markdown("📊 **Eagan DataTool**")
    st.sidebar.markdown("*Powered by N2G*")
    st.sidebar.markdown("Eagan DataTool is an all-encompassing solution designed to facilitate end-to-end data management and analytics processes.",unsafe_allow_html=True)

def get_gemini_model(data_file, query):
    
    prompt = f"""
    Act as a data analyst, 
    who gives insights from the data provided, you will explain in simple and easy to understand words about the provided data. 
    I will provide you with data, just explain your findings.
    
    Data: {data_file}\n
    Question: {query}\n
    
    Give a proper detailed answer. 
    Dont give many questions and answers simulateously. 
    Only explain what you see in the provided data. Dont answer anything else.
    Explain in points
    
    """
    
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(prompt)
    
    return response.text

# Function main
def main():
    set_page_configuration()
    sidebar()
    st.markdown("<h1 style='text-align: center; color: black;'> 📊 Eagan DataTool</h1>", unsafe_allow_html=True)
    st.markdown("---")
    # Filter selection
    selected = option_menu(
        None, 
        options = ['Clients', 'Projects', 'Tasks', 'Employees', 'Resourcing','Data GenAI'],
        icons=['gear', 'graph-up-arrow', 'info', 'people', 'activity','globe'],
        orientation="horizontal"
        )
    
    # Dictionary mapping each option to its subheader and description
    option_info = {
        'Clients': {
            'subheader': 'Client Details',
            'description': "This section lists the clients associated with the projects. It includes information such as the client's name, contact person, email, phone number etc."
        },
        'Projects': {
            'subheader': 'Project Details',
            'description': "This section contains details about the projects being tracked. It includes project ID, name, associated client, start date, end date, and current status."
        },
        'Tasks': {
            'subheader': 'Task Details',
            'description': "This section lists the tasks associated with each project. It includes task ID, project ID, task description, assigned employee, start date, due date, and status of completion."
        },
        'Employees': {
            'subheader': 'Employee Details',
            'description': "This section contains information about the employees involved in the project. It includes employee ID, name, email, phone number, department, and position within the organization."
        },
        'Resourcing': {
            'subheader': 'Resourcing',
            'description': "This section tracks the allocation of resources to tasks within projects. It includes project ID, task ID, employee ID, start date of assignment, and end date of assignment for each resource."
        }
    }
    
    file_path = "Project Tracking Tool.xlsx"
    data = pd.ExcelFile(file_path)
    sheet_names = data.sheet_names

    if selected in option_info:
        option = option_info[selected]
        st.subheader(option['subheader'])
        st.markdown(option['description'], unsafe_allow_html=True)
        individual_data = data.parse(selected, usecols=None, skiprows=4).dropna(axis=0, how='all').dropna(axis=1, how='all')
        AgGrid(individual_data, editable=True, theme='alpine')
    
    elif selected == 'Data GenAI':
        st.subheader("Chat with Data - beta version")
        st.markdown("Data provided by the Language Model (LLM) is used for information purposes. Please use it carefully as it may not always be accurate. Verify important details from reliable sources before making decisions based on this data.", unsafe_allow_html=True)
        selectbox = st.selectbox("Select Sheet", sheet_names)
        individual_data = data.parse(selectbox, usecols=None, skiprows=4).dropna(axis=0, how='all').dropna(axis=1, how='all')
        st.write(individual_data)
        
        with st.form("API key"):
            key = st.text_input("**Google Gemini Key**", value="", type="password")
            if st.form_submit_button("Submit"):
                
                genai.configure(api_key=key)
                os.environ['GOOGLE_API_KEY'] = key

        with st.form("Question"):
            ## Initialize chat interface
            user_input = st.text_input("Ask a Question:")
            
            if st.form_submit_button("Submit"):
                st.markdown("**Using Direct Gemini**", unsafe_allow_html=True)
                response2 = get_gemini_model(individual_data, user_input)
                st.write(response2)          
    else:
        pass
     
if __name__ == "__main__":
    main()
    

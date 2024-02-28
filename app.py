import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid

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
def sidebar(sheet_selected):
    st.sidebar.image("Logo2.jpg", width=100)
    st.sidebar.markdown("📊 **Eagan DataTool**")
    st.sidebar.markdown("*Powered by N2G*")
    st.sidebar.markdown("Eagan DataTool is an all-encompassing solution designed to facilitate end-to-end data management and analytics processes.",unsafe_allow_html=True)
    file_path = "Project Tracking Tool.xlsx"
    data = pd.ExcelFile(file_path)
    return data.parse(sheet_selected, usecols=None, skiprows=4).dropna(axis=0, how='all').dropna(axis=1, how='all')

# Function main
def main():
    set_page_configuration()
    st.markdown("<h1 style='text-align: center; color: black;'> 📊 Eagan DataTool</h1>", unsafe_allow_html=True)
    st.markdown("---")
    # Filter selection
    selected = option_menu(
        None, 
        options = ['Clients', 'Projects', 'Tasks', 'Employees', 'Resourcing'],
        icons=['gear', 'graph-up-arrow', 'info', 'people', 'activity'],
        orientation="horizontal"
        ) 
    
    data = sidebar(selected)
    
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
            
    # Display the selected option's subheader, description, and AgGrid
    option = option_info[selected]

    st.subheader(option['subheader'])
    st.markdown(option['description'], unsafe_allow_html=True)
    AgGrid(data, editable=True)
  
      
if __name__ == "__main__":
    main()
    
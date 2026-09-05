import streamlit as st
from components.employee_search import employee_search

def show_sidebar(df):
    st.sidebar.title("Dashboard filters")
    search_query=employee_search()
    selected_department=st.sidebar.selectbox("Department",["All"]+sorted(df["department_name"].unique().tolist()))
    selected_gender=st.sidebar.selectbox("Gender",["All"]+sorted(df["gender"].unique().tolist()))
    selected_location=st.sidebar.selectbox("Location",["All"]+sorted(df["location_name"].unique().tolist()))
    return(
        search_query,
        selected_department,
        selected_gender,
        selected_location
    )
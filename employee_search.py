import streamlit as st
def employee_search():
    search_query=st.text_input("🔍 Search Employee",
                               placeholder="Search by name,employee code,email...")
    return search_query

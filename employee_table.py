import streamlit as st
def show_employee_table(df):
    st.subheader("👨‍💼 Employee Records")
    st.dataframe(df,use_container_width=True,hide_index=True)

import streamlit as st

def show_kpi_card(icon,value,title):
    html=f"""
    <div class="kpi-card">
      <div class="kpi-icon">
         {icon}
     </div>
     <div class="kpi-value">
     {value}
</div>
    <div class="kpi-title">
    {title}
</div>
"""
    st.markdown(html,unsafe_allow_html=True)
    
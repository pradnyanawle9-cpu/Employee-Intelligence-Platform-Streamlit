# ==========================================
# EMPLOYEE INTELLIGENCE PLATFORM
# WORKFORCE ANALYTICS DASHBOARD
# ==========================================

import streamlit as st
import pandas as pd

# ==========================================
# IMPORT COMPONENTS
# ==========================================

from data.cleaning import clean_employee_data
from services.employee_service import update_employee
from components.kpi_cards import show_kpi_card
from components.sidebar import show_sidebar
from components.charts import department_chart
from components.status_chart import employee_status_chart
from components.experience_chart import experience_chart
from components.location_chart import location_chart
from components.salary_chart import salary_chart
from components.experience_salary_chart import experience_salary_chart
from services.delete_employee_service import delete_employee

# ==========================================
# DATABASE
# ==========================================

from db import get_connection

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Employee Intelligence Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD CSS
# ==========================================

def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as css_file:
            st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# ==========================================
# LOAD EMPLOYEE DATA
# ==========================================

@st.cache_data(show_spinner=False)
def load_data():
    connection = get_connection()
    try:
        query = """
        SELECT
            e.employee_id,
            e.employee_code,
            e.first_name,
            e.last_name,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            e.gender,
            e.email,
            e.phone,
            d.department_name,
            jr.role_name,
            l.location_name,
            l.city,
            e.experience_years,
            e.basic_salary,
            e.employee_status,
            e.date_of_birth,
            e.hire_date
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.department_id
        INNER JOIN job_roles jr ON e.role_id = jr.role_id
        INNER JOIN locations l ON e.location_id = l.location_id
        """
        df = pd.read_sql(query, connection)
        df = clean_employee_data(df)
        return df
    finally:
        connection.close()

df = load_data()

# ==========================================
# SIDEBAR FILTERS
# ==========================================

(
    search_query,
    selected_department,
    selected_gender,
    selected_location
) = show_sidebar(df)

# ==========================================
# FILTERED DATA
# ==========================================

filtered_df = df.copy()

if search_query:
    search_query = search_query.strip().lower()
    searchable_columns = [
        "employee_code", "employee_name", "email",
        "phone", "department_name", "role_name", "location_name"
    ]
    existing_columns = [col for col in searchable_columns if col in filtered_df.columns]

    filtered_df = filtered_df[
        filtered_df[existing_columns]
        .astype(str)
        .apply(
            lambda row: row.str.lower().str.contains(search_query, na=False).any(),
            axis=1
        )
    ]

if selected_department != "All":
    filtered_df = filtered_df[filtered_df["department_name"] == selected_department]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]

if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location_name"] == selected_location]

# ==========================================
# HERO SECTION
# ==========================================

st.title("💼 Employee Intelligence Platform")
st.caption("Enterprise Workforce Analytics Dashboard")
st.divider()

# ==========================================
# WORKFORCE OVERVIEW
# ==========================================

st.subheader("Workforce Overview")

total_employees = len(filtered_df)
total_departments = filtered_df["department_name"].nunique() if not filtered_df.empty else 0
total_locations = filtered_df["location_name"].nunique() if not filtered_df.empty else 0
avg_salary = filtered_df["basic_salary"].mean() if not filtered_df.empty else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    show_kpi_card(icon="👨‍💼", value=f"{total_employees:,}", title="Total Employees")
with col2:
    show_kpi_card(icon="🏢", value=f"{total_departments:,}", title="Departments")
with col3:
    show_kpi_card(icon="📍", value=f"{total_locations:,}", title="Locations")
with col4:
    show_kpi_card(icon="💰", value=f"₹{avg_salary:,.0f}", title="Average Salary")

st.divider()

# ==========================================
# WORKFORCE ANALYTICS
# ==========================================

st.header("📊 Workforce Analytics")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    department_chart(df, selected_department)
with chart_col2:
    employee_status_chart(filtered_df)

st.divider()

chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    experience_chart(filtered_df)
with chart_col4:
    location_chart(df, selected_location)

st.divider()

# ==========================================
# COMPENSATION ANALYTICS
# ==========================================

st.header("💰 Compensation Analytics")

salary_col, experience_salary_col = st.columns(2)
with salary_col:
    salary_chart(df)
with experience_salary_col:
    experience_salary_chart(filtered_df)

st.divider()

# ==========================================
# EMPLOYEE RECORDS CONTROLS
# ==========================================

st.subheader("👨‍💼 Employee Records")

# State Management for UI Toggles
if "show_add_employee" not in st.session_state:
    st.session_state["show_add_employee"] = False

if "show_delete_employee" not in st.session_state:
    st.session_state["show_delete_employee"] = False

col_add, col_del = st.columns(2)

with col_add:
    if st.button("➕ Add New Employee", key="open_add_employee_button"):
        st.session_state["show_add_employee"] = not st.session_state["show_add_employee"]
        st.session_state["show_delete_employee"] = False

with col_del:
    if st.button("🗑 Delete Employee", key="delete_employee_button"):
        st.session_state["show_delete_employee"] = not st.session_state["show_delete_employee"]
        st.session_state["show_add_employee"] = False

# ==========================================
# ADD NEW EMPLOYEE FORM
# ==========================================

if st.session_state["show_add_employee"]:

    st.subheader("➕ Add New Employee Form")

    with st.form("add_employee_form", clear_on_submit=False):

        form_col1, form_col2 = st.columns(2)

        with form_col1:
            first_name = st.text_input("First Name *")
            last_name = st.text_input("Last Name *")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            email = st.text_input("Email *")
            phone = st.text_input("Phone *")
            department_id = st.number_input("Department ID", min_value=1, value=1, step=1)
            role_id = st.number_input("Role ID", min_value=1, value=1, step=1)

        with form_col2:
            location_id = st.number_input("Location ID", min_value=1, value=1, step=1)
            experience_years = st.number_input("Experience Years", min_value=0.0, value=0.0, step=0.5)
            basic_salary = st.number_input("Basic Salary", min_value=0.0, value=30000.0, step=1000.0)
            employee_status = st.selectbox("Employee Status", ["Active", "Inactive", "On Leave", "Resigned"])
            hire_date = st.date_input("Hire Date")
            date_of_birth = st.date_input("Date of Birth")

        save_employee = st.form_submit_button("💾 Save Employee")

        if save_employee:
            if not first_name.strip() or not last_name.strip() or not email.strip() or not phone.strip():
                st.error("⚠️ Please fill all required (*) fields.")
            else:
                conn = None
                cur = None
                try:
                    conn = get_connection()
                    cur = conn.cursor()

                    cur.execute("SELECT COUNT(*) FROM employees WHERE email=%s", (email.strip(),))
                    if cur.fetchone()[0] > 0:
                        st.error("❌ Email already exists in Database!")
                    else:
                        cur.execute("SELECT employee_code FROM employees ORDER BY employee_id DESC LIMIT 1")
                        last_emp = cur.fetchone()

                        if last_emp and last_emp[0]:
                            last_code = last_emp[0]
                            num_part = ''.join(filter(str.isdigit, last_code))
                            next_num = int(num_part) + 1 if num_part else 1
                            employee_code = f"EMP{next_num:05d}"
                        else:
                            employee_code = "EMP00001"

                        insert_query = """
                        INSERT INTO employees
                        (
                            employee_code, first_name, last_name, gender, email,
                            phone, department_id, role_id, location_id,
                            date_of_birth, hire_date, experience_years, basic_salary, employee_status
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """

                        values = (
                            employee_code,
                            first_name.strip(),
                            last_name.strip(),
                            gender,
                            email.strip(),
                            phone.strip(),
                            int(department_id),
                            int(role_id),
                            int(location_id),
                            date_of_birth,
                            hire_date,
                            float(experience_years),
                            float(basic_salary),
                            employee_status
                        )

                        cur.execute(insert_query, values)
                        conn.commit()

                        st.success(f"✅ Employee {employee_code} Added Successfully!")
                        st.session_state["show_add_employee"] = False
                        st.cache_data.clear()
                        st.rerun()

                except Exception as ex:
                    if conn:
                        conn.rollback()
                    st.error(f"❌ Database Error: {str(ex)}")
                finally:
                    if cur:
                        cur.close()
                    if conn:
                        conn.close()

# ==========================================
# DELETE EMPLOYEE UI & LOGIC
# ==========================================

if st.session_state["show_delete_employee"]:

    st.subheader("🗑 Delete Employee")

    # Dropdown Options
    employee_options = (
        filtered_df["employee_code"] + " - " + filtered_df["employee_name"]
    ).tolist()

    if employee_options:
        selected_delete = st.selectbox("Select Employee to Delete", employee_options)
        employee_code = selected_delete.split(" - ")[0]
        
        employee_matches = filtered_df[filtered_df["employee_code"] == employee_code]

        if not employee_matches.empty:
            employee_row = employee_matches.iloc[0]

            col_confirm, col_cancel = st.columns(2)

            with col_confirm:
                if st.button("✅ Confirm Delete", key="confirm_delete_btn"):
                    success = delete_employee(employee_row["employee_id"])
                    if success:
                        st.success("✅ Employee Deleted Successfully!")
                        st.session_state["show_delete_employee"] = False
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete employee. Foreign Key Constraint error.")

            with col_cancel:
                if st.button("❌ Cancel", key="cancel_delete_btn"):
                    st.session_state["show_delete_employee"] = False
                    st.rerun()
    else:
        st.warning("No employees available to delete.")

# ==========================================
# EMPLOYEE RECORDS DISPLAY
# ==========================================

st.divider()

table_df = filtered_df.copy()

st.caption(f"Total Records : {len(table_df)}")

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)
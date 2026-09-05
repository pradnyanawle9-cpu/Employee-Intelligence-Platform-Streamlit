# ==========================================
# EMPLOYEE SERVICE
# ==========================================

from db import get_connection


def update_employee(
    employee_id,
    first_name,
    last_name,
    email,
    phone,
    experience_years,
    basic_salary,
    employee_status
):
    """
    Updates employee information in database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    UPDATE employees
    SET

        first_name=%s,
        last_name=%s,
        email=%s,
        phone=%s,
        experience_years=%s,
        basic_salary=%s,
        employee_status=%s

    WHERE employee_id=%s
    """

    values = (

        str(first_name),
        str(last_name),
        str(email),
        str(phone),
        float(experience_years),
        float(basic_salary),
        str(employee_status),
        int(employee_id)

    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()

    connection.close()

    return True
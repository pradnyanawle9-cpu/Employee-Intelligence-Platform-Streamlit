from db import get_connection
def delete_employee(employee_id):
    """Permanently Delete an employee"""
    connection=get_connection()
    cursor=connection.cursor()
    query="""DELETE FROM employees Where employee_id=%s"""
    cursor.execute(query,(int(employee_id),))
    connection.commit()
    deleted=cursor.rowcount
    cursor.close()
    connection.close()
    return deleted>0
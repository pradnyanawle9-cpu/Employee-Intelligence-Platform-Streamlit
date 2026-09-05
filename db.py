# ==========================================
# Employee Intelligence Platform
# Database Connection
# ==========================================

import mysql.connector
from mysql.connector import Error


def get_connection():

    try:

        connection = mysql.connector.connect(

            host="localhost",
            user="root",
            password="Pradnya@114",
            database="employee_analytics_db"

        )

        return connection


    except Error as e:

        print(f"❌ Database Connection Error : {e}")

        return None
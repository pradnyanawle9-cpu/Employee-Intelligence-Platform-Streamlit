from db import get_connection


connection = get_connection()

if connection:

    print("🎉 Connection Test Passed")

    connection.close()

    print("🔒 Database Connection Closed")

else:

    print("❌ Unable to Connect Database")
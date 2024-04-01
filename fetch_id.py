import psycopg2

def get_user_id(username):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgresamdqdp1403',
            dbname='postgres'
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Execute SQL query to retrieve user ID based on username
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()

        if user_id:
            return user_id[0]  # Return the user ID
        else:
            print(f"User '{username}' not found.")
            return None

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


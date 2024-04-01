import streamlit as st
import psycopg2

def login():
    st.write("Login")

    # Check if username and password are already stored in session
    if not st.session_state.get('username'):
        # If not, ask user to enter their username and password
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")

        
        
        # Check if user exists in the database
        user_id = check_user_credentials(username, password)
        if user_id:
            # If user exists, set the session state with the username and user_id
            st.session_state['username'] = username
            st.session_state['user_id'] = user_id
            st.write("Welcome back, " + username)
        else:
            st.error("Invalid username or password. Please try again.")
    else:
        # If username is already stored in session, display it
        st.write("Welcome back, " + st.session_state['username'])

def check_user_credentials(username, password):
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

        # Query the database to check if user exists with provided username and password
        cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user_id = cursor.fetchone()

        if user_id:
            return user_id[0]  # Return the user ID
        else:
            return None

    except Exception as e:
        st.warning(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import streamlit as st
from face import memorize_face
def signup():
    with st.form("my_form"):
        st.write("Join with us Today !!")

        name = st.text_input('Your Username')
        password = st.text_input('Your Password (Minimum length - 6 letters)', type='password')
        country = st.text_input('Your Country')
        email = st.text_input('Enter your email')
        phone_number = st.text_input('Your Phone Number')

        checkbox_val = st.checkbox("Form checkbox")


        uploaded_image = st.camera_input("Choose a picture for face detection")
        if uploaded_image:
                    st.write("Uploading face to server...")
                    memorize_face(name, uploaded_image)
        else:
                    st.warning("Upload Image for face detection")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:

            if 'username' not in st.session_state or st.session_state.username=='':
                st.session_state['username'] = name

            st.write(st.session_state.username)

            st.write("slider", "checkbox", checkbox_val)

            # Insert user data into the database
            insert_user_into_database(name, password, email, country, phone_number)

    st.warning('If already Logged in, log out first to change to other account')

def insert_user_into_database(username, password, email, country, phone_number):
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

        # Insert user data into the users table
        cursor.execute("INSERT INTO users (username, password, email, country_of_residence, phone_number) VALUES (%s, %s, %s, %s, %s)",
                       (username, password, email, country, phone_number))

        # Commit the changes
        connection.commit()

        st.success(f"User '{username}' signed up successfully.")

        if not st.session_state.get('username'):
            # If not, ask user to enter their name
            username_ = username
            
            # Store username in session
            st.session_state['username'] = username_

    except Exception as e:
        st.warning(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


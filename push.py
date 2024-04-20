import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import streamlit as st
import uuid
from fetch_id import get_user_id


def insert_file_into_database(file_content, filename, connection_params, password, list_uuid):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(**connection_params)

        # Set isolation level to autocommit for creating the database
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object
        cursor = connection.cursor()

                # Create a table to store file data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                file_content BYTEA,
                password VARCHAR(255),
                user_id INT
            )
        """)
        username = st.session_state['username']

        userid = get_user_id(username)

        

        # Check if the file with the same filename and user_id already exists
        cursor.execute("SELECT id FROM files WHERE filename = %s AND user_id = %s", (filename, userid))
        existing_file_id = cursor.fetchone()

        if existing_file_id:
            st.warning(f"File with the same name and user ID already exists. Please choose a different filename.")
            return



        # Create a uuid database
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uuids (
                id SERIAL PRIMARY KEY,
                fileid INT,
                uuid VARCHAR(36) 
            )
        """)

        # Insert the file content into the database
        cursor.execute("INSERT INTO files (filename, file_content, password, user_id) VALUES (%s, %s, %s, %s)",
                       (filename, file_content, password, userid))

        # Get the ID of the inserted file
        cursor.execute("SELECT id FROM files WHERE filename = %s AND user_id = %s", (filename, userid))
        file_id = cursor.fetchone()[0]

        # Insert UUIDs into the uuids table
        for uuid_val in list_uuid:
            cursor.execute("INSERT INTO uuids (fileid, uuid) VALUES (%s, %s)", (file_id, uuid_val))

        # Commit the changes
        connection.commit()

        st.success(f"File '{filename}' (ID: {file_id}) inserted into the database.")

    except Exception as e:
        st.warning(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def file(uploaded_file_buffer, filename):  # Pass BytesIO buffer instead of uploaded_file

    password = st.text_input('Enter your Password')

    connection_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgresamdqdp1403',
        'dbname': 'postgres'
    }

    system_uuid = str(uuid.UUID(int=uuid.getnode()))

    list_uuid = [system_uuid,]

    st.title('Enter uuids of computer you want to access it from')
    st.info('By default only this system will be considered')

    col1,col2 = st.columns((2))
    col3,col4,col5 = st.columns(3)

    with st.container():
        with col3:
            uuid1=st.text_input('Enter first uuid')
        with col4:
            uuid2=st.text_input('Enter second uuid')
        with col5:
            uuid3=st.text_input('Enter third uuid')

    if(uuid1!=''):
        list_uuid.append(uuid1)
    if(uuid2!=''):
        list_uuid.append(uuid2)
    if(uuid3!=''):
        list_uuid.append(uuid3)



    if st.button('Push File to postgres') and uploaded_file_buffer is not None:
        # Use the provided BytesIO buffer directly
        insert_file_into_database(uploaded_file_buffer, filename, connection_params, password, list_uuid)

    # if st.button('UUID'):
    #     st.write("System UUID:", system_uuid)


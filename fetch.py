import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import streamlit as st
import uuid
import io
import bson
import sympy
from elgamal import decrypt_by_elgamal
from encrypt import power
from decrypt import main_dec_demo
from location import location
from datetime import datetime
from elgamal import fetch_details
from rsa import decryption_by_rsa
from fetch_id import get_user_id

def fetch_elgamal(user_id, file_name, password, p_key, key, p):

    username = st.session_state['username']

    loc,reg = location()

    st.success(loc)

    lat, lon = loc.split(',')
    lat = float(lat)  
    lon = float(lon)

    system_uuid = str(uuid.UUID(int=uuid.getnode()))

    connection_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgresamdqdp1403',
        'dbname': 'postgres'
    }

    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(**connection_params)

        # Set isolation level to autocommit for creating the database
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object
        cursor = connection.cursor()

        # Check if the file with the specified criteria exists
        cursor.execute("SELECT file_content FROM files WHERE filename = %s AND password = %s AND user_id = %s",
                       (file_name, password, user_id))
        file_content_bson = cursor.fetchone()

        if not file_content_bson:
            st.warning("File not found with the specified criteria.")
            return None

        # Convert the BSON data to a list of numbers
        file_content_buffer = io.BytesIO(file_content_bson[0])
        numbers_list = bson.loads(file_content_buffer.read())
        numbers_list = numbers_list.get('data', []) 


        key = int(key)

        # st.write("Encrypted number list", numbers_list)

        # Check if system_uuid is present in uuids table for the given file_id
        cursor.execute("SELECT fileid FROM uuids WHERE uuid = %s", (system_uuid,))
        associated_file_ids = [row[0] for row in cursor.fetchall()]

        if not any(associated_file_ids):
            st.warning(f"System UUID {system_uuid} is not associated with any file.")
            return None


        st.info(numbers_list)
        # st.write("FFFFF",q,p_key,key)   
        decrypted_message = decrypt_by_elgamal(numbers_list, p_key, key, p)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert into history table
        cursor.execute("INSERT INTO history (filename, username, region, time_, lat, lon) VALUES (%s, %s, %s, %s, %s, %s)",
                       (file_name, username, reg, current_time, lat, lon))
        connection.commit()


        return decrypted_message

    except Exception as e:
        st.warning(f"Error: {e}")
        return None

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetch_rsa(user_id, file_name, password, key, n):
    username = st.session_state['username']

    loc,reg = location()

    st.success(loc)

    lat, lon = loc.split(',')
    lat = float(lat)  
    lon = float(lon)

    system_uuid = str(uuid.UUID(int=uuid.getnode()))

    connection_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgresamdqdp1403',
        'dbname': 'postgres'
    }

    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(**connection_params)

        # Set isolation level to autocommit for creating the database
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object
        cursor = connection.cursor()

        # Check if the file with the specified criteria exists
        cursor.execute("SELECT file_content FROM files WHERE filename = %s AND password = %s AND user_id = %s",
                       (file_name, password, user_id))
        file_content_bson = cursor.fetchone()

        if not file_content_bson:
            st.warning("File not found with the specified criteria.")
            return None

        # Convert the BSON data to a list of numbers
        file_content_buffer = io.BytesIO(file_content_bson[0])
        numbers_list = bson.loads(file_content_buffer.read())
        numbers_list = numbers_list.get('data', []) 


        key = int(key)

        # st.write("Encrypted number list", numbers_list)

        # Check if system_uuid is present in uuids table for the given file_id
        cursor.execute("SELECT fileid FROM uuids WHERE uuid = %s", (system_uuid,))
        associated_file_ids = [row[0] for row in cursor.fetchall()]

        if not any(associated_file_ids):
            st.warning(f"System UUID {system_uuid} is not associated with any file.")
            return None


        
        # st.write("FFFFF",q,p_key,key)   
        decrypted_message = decryption_by_rsa(numbers_list, key, n)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert into history table
        cursor.execute("INSERT INTO history (filename, username, region, time_, lat, lon) VALUES (%s, %s, %s, %s, %s, %s)",
                       (file_name, username, reg, current_time, lat, lon))
        connection.commit()


        return decrypted_message

    except Exception as e:
        st.warning(f"Error: {e}")
        return None

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

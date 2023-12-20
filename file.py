import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import streamlit as st

def insert_file_into_database(file_path, connection_params):
    try:
        # Establish a connection to the PostgreSQL server
        connection = psycopg2.connect(**connection_params)
        
        # Set isolation level to autocommit for creating the database
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object
        cursor = connection.cursor()

        # Create a database (if it doesn't exist)
        database_name = connection_params['dbname']
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))

        # Switch to the newly created database
        connection.close()
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Create a table to store file data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                file_content BYTEA
            )
        """)

        # Read the file content
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # Insert the file content into the database
        cursor.execute("INSERT INTO files (filename, file_content) VALUES (%s, %s)",
                       (file_path, file_content))

        # Commit the changes
        connection.commit()

        print(f"File '{file_path}' inserted into the database.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Example usage:
file_path = '/text.txt'
connection_params = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgresamdqdp1403',
    'dbname': 'postgres'
}

insert_file_into_database(file_path, connection_params)

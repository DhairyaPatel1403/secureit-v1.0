import streamlit as st
import psycopg2
import pandas as pd

def history():

    username = st.session_state['username']

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

        # Create a cursor object
        cursor = connection.cursor()

        # Fetch data from the history table
        cursor.execute("SELECT * FROM history WHERE name = %s", (username,))
        rows = cursor.fetchall()

        if not rows:
            st.warning("No data found in the history table.")
        else:
            # Display each row one by one in a box format
            st.write("History Table:")

            df = pd.DataFrame(rows, columns=['id', 'filename', 'username', 'region', 'time_', 'lat', 'lon'])


            for row in rows:

                col1, col2 = st.columns(2)

                with st.container():
                    with col1:
                        st.info({
                            'ID': row[0],
                            'Filename': row[1],
                            'Username': row[2],
                            'Region': row[3],
                            'Time': row[4],
                            'Latitude': row[5],
                            'Longitude': row[6]
                        })
                    # Create a DataFrame with latitude and longitude columns
                    df = pd.DataFrame([[row[5], row[6]]], columns=['lat', 'lon'])
                    with col2:
                        st.map(df)


    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

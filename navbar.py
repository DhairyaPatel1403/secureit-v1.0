import streamlit as st
from flask import Flask, request
import requests
import socket
import platform
import netifaces
import json
from logout import logout

# Function to render different pages
def render_page(page_name):
    if page_name == 'Login':
        # Import and execute code from page1.py
        from login import login
        login()
    if page_name == 'Signup':
        # Import and execute code from page1.py
        from signup import signup
        signup()
    if page_name == 'Log Out':
        # Import and execute code from page1.py
        from logout import logout
        logout()
    if page_name == 'History':
        # Import and execute code from page1.py
        from history import history
        history()
    if page_name == 'LockFile':
        # Import and execute code from page1.py
        from lockfile import lockfile
        lockfile()
    if page_name == 'UnlockFile':
        # Import and execute code from page1.py
        from unlockfile import unlockfile
        unlockfile()



# Streamlit app
def main():

    if 'userip' not in st.session_state:
        response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=1a7ac43f33da4a8dbb17097848197588&ip_address=")
        st.write(response.status_code)
        st.write(response.content)
        response_json = json.loads(response.content)

        # Extracting the ip_address
        ip_address = response_json["ip_address"]


        user_ip = ip_address
        user_device = platform.node()
        interfaces = netifaces.interfaces()


        # Make a request to the Flask API to log in the user
        api_url = 'http://localhost:8002/login'  # Adjust the URL if necessary
        response = requests.post(api_url, json={"ip_address": user_ip, "user_device":user_device, "network_interfaces":interfaces})

        # Check if the login was successful
        if response.status_code == 200:
            
            # Store the user's IP address in the session state
            st.session_state.userip = user_ip
        else:
            pass

    col1, col2 = st.columns(2)

    with col1:
        st.title(''' Secure:orange[It] ''')
    with col2:
        if st.session_state.get('username'):
            logout()



    # Create a navigation bar
    pages = ['Login', 'Signup', 'Log Out', 'History', 'LockFile', 'UnlockFile']
    selected_page = st.sidebar.selectbox('Select Page', pages)

    # Render the selected page
    render_page(selected_page)

if __name__ == '__main__':
    
    main()

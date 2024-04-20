import streamlit as st
import math
import sympy
import io
import bson
import random
import requests
import json
from fetch import fetch_elgamal
from face import detect
from fetch import fetch_rsa
from fetch_id import get_user_id
import datetime
import numpy as np
from io import BytesIO
import base64
import zlib
import binascii
from PIL import Image



def fetch_details(filename, username, cipher_name):
    url = 'http://127.0.0.1:5000/details'
    response = requests.get(url)

    if response.status_code == 200:
        # st.write(filename, username, cipher_name)
        data = response.json().get('details', [])
        # st.write(data)
        if data:
            for item in data:
                if item.get('name') == cipher_name and item.get('filename') == filename and item.get('username') == username:
                    # st.write('Details found for name', filename , username)
                    return item
            st.warning('No details found for filename')
            return None
        else:
            st.warning("No data returned from the server")
            return None
    else:
        print('Failed to fetch details. Status code:', response.status_code)
        return None
    

def unlockimg():
    st.title('Unlock Your Image')

    username = st.session_state['username']

    filename = st.text_input('Enter File Name')
    password = st.text_input('Enter Password')

    key = st.text_input('Enter Key')

    if key:
        key = int(key)

        name = detect()

        username = st.session_state['username']

        userid = get_user_id(username)

        if username==name:

            st.info(username)

            if (key < 462580593179):

                item = fetch_details(filename, username, 'RSA')

                st.info(item)

                key,n = item.get('key'), item.get('n')
                key=int(key)
                n=int(n)

                decrypted_msg = fetch_rsa(userid, filename, password, key, n)

                if decrypted_msg is None:
                    st.warning('No image')
                    pass
                    # st.warning("Warning will be sent to user.")
                    # url = "https://formspree.io/f/xgegvqaa"
                    # current_datetime = datetime.datetime.now()

                    # # Format the date and time as a string
                    # current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    # data = {
                    #     "email": "dpvp1403@gmail.com",  # Replace with the actual email address
                    #     "message": f"User {username} tried to open file {filename} at - {current_datetime_str}."  # Replace with the actual message
                    # }
                    # response = requests.post(url, data=data)


                else:
                    st.warning('Showing Image')

                    image_bytes = base64.b64decode(decrypted_msg)
                    # Convert bytes to a PIL Image
                    image = Image.open(io.BytesIO(image_bytes))
                    # Display the image in Streamlit
                    st.image(image, caption='Uploaded Image')

            else:
                item = fetch_details(filename, username, 'Elgamal')

                st.info(item)

                p,p1,q,h = item.get('p'), item.get('p1'), item.get('q'), item.get('h')

                p = int(p)
                p1 = int(p1)

                decrypted_msg = fetch_elgamal(userid, filename, password, p1, key, p)

                image_bytes = base64.b64decode(decrypted_msg)
                # Convert bytes to a PIL Image
                image = Image.open(io.BytesIO(image_bytes))
                # Display the image in Streamlit
                st.image(image, caption='Uploaded Image')

        else:
            st.warning("Face undetectable")
            # st.write(username)
import streamlit as st
import math
import sympy
import io
import bson
import random
import requests
import json
from push import file




def power(a, b, c):
    x = 1
    y = a
 
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)
 
    return x % c


def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def encrypted_by_rsa(msg, e, n):
    c = power(msg, e, n)
    return c

def decryption_by_rsa(msg, d, n):
    ans = ""
    for c in msg:
        m = power(c,d,n)
        ans += chr(m)  # Concatenate decrypted characters to form a string
    return ans


def rsa(str_msg, d, p, q, e):
    # st.header("By RSA")

    n = p*q

    encr_list = []

    st.warning(f"p, q, n, e, d - {p}, {q}, {n}, {e}, {d}")

    filename = st.text_input('Give your encrypted file a name.')

    if filename!="":

        for i in str_msg:
            c = encrypted_by_rsa(ord(i), e, n)
            encr_list.append(c)

        # st.write("Encrypted message =", encr_list)

        key = d

        details=[key, n, filename, 'userid35']
        pushed = add_name("RSA", details)


        if pushed:
        
            item = fetch_details('RSA', 'userid35', filename)
        
            n = item.get('n')

            n = int(n)
            decry_msg = decryption_by_rsa(encr_list, key, n)
            st.write("Decrypted message =", decry_msg)


            data_dict = {"data": encr_list}
        
            # Convert the dictionary to BSON format
            bson_data = bson.dumps(data_dict)

            # Create a BytesIO buffer to hold the BSON data
            buffer = io.BytesIO(bson_data)

            # Create a download button
            st.download_button(
                label="Download Encrypted List",
                key="download_encrypted_list",
                data=bson_data,
                file_name="encrypted_list_elgamal.bson",
                mime="application/octet-stream",
            )

            file(bson_data, filename)


def add_name(cipher_name, details):
    url = 'http://localhost:5000/details'  # Replace with your server URL
    headers = {'Content-Type': 'application/json'}

    # Extract parameters from details
    key, n, filename, username = details[:4]  # Assuming details contains key, n, filename, and username

    # Check if data with the same key, filename, and username already exists
    if check_existing_key_filename_username(key, filename, username):
        st.warning('Details with the same key, filename, and username already exist')
        return True

    # Prepare data to be sent to the server
    data = {'cipher_name': cipher_name, 'key': key, 'n': n, 'filename': filename, 'username': username}

    st.write(data)

    # Push the data to the server
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        st.success('Details added successfully')
        return True
    else:
        st.warning('Failed to add details')
        return False

def check_existing_key_filename_username(key, filename, username):
    url = 'http://localhost:5000/details'  # Replace with your server URL
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get('details', [])
        for item in data:
            if item.get('filename') == filename and item.get('username') == username:
                return item
    else:
        st.warning('Failed to fetch existing data')
        return None


def check_existing_key(key, filename, username):
    url = 'http://localhost:5000/details'  # Replace with your server URL
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get('details', [])
        for item in data:
            if item.get('key') == key and item.get('filename') == filename and item.get('username') == username:
                return True
    else:
        st.warning('Failed to fetch existing data')
    return False



def fetch_details(cipher_name, username, filename):
    url = 'http://127.0.0.1:5000/details'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get('details', [])
        for item in data:
            if item.get('username') == username and item.get('name') == cipher_name  and item.get('filename') == filename:
                return item
        print('No details found for file and user ', filename, username)
        return None, None, None, None
    else:
        print('Failed to fetch details. Status code:', response.status_code)
        return None, None, None, None
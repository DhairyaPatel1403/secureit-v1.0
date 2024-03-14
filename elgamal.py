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


def gen_key_e(q):  #generate private key for sender
 
    key = random.randint(0, q)
    while math.gcd(q, key) != 1:
        key = random.randint(0, q)
 
    return 655 


def encrypt_by_elgamal(msg, p, h, q):
 
    en_msg = []
    en_n_message=[]
 
    k = gen_key_e(p) # Private key for sender
    s = power(h, k, p)
    p = power(q, k, p)
     
    for i in range(0, len(msg)):
        en_msg.append(msg[i])
 
    print("g^k used : ", p)
    print("g^ak used : ", s)
    for i in range(0, len(en_msg)):
        en_n_message.append(s * ord(en_msg[i]))
 
    return en_n_message, p

def decrypt_by_elgamal(en_msg, p_1, key, p):

    dr_msg = []
    h = power(p_1, key, p)
    st.write("h",h)
    st.write("Message list from decryption ", en_msg)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i]/h)))

    dmsg = ''.join(dr_msg)
         
    return dmsg


def elgamal(str_msg, d, p, q, e):
    # key exchange using diffie hellman and elgamal algorithm
    # st.header("ElGamal")

    #in elgamal decryption, p and q are important not key
    # here the q key becomes - g

    #elgamal(str_msg, d, p, q)

    st.info("Elgamal")

    filename = st.text_input('Give your encrypted file a name.')

    st.info(f"Key is - {d}" )

    key = d

    if(filename!=""):
        key = int(key)

        st.write("The key inputed is ", key)

        h = power(q, key, p)

        st.write("Key going in encryption - ", key)
        en_msg, p_1 = encrypt_by_elgamal(str_msg, p, h, q)
        st.write("Keep this key as p_1_key - ", p_1)
        print("Encrypted MEssage - ", en_msg)


        details=[p_1, p, h, q, key, filename, 'userid35', en_msg]
        success=False
        success = add_name("Elgamal", details)


        if success:
            item = fetch_details(key, 'Elgamal')
            p,p1,q,h = item.get('p'), item.get('p1'), item.get('q'), item.get('h')
            en_msg, p_1 = encrypt_by_elgamal(str_msg, p, h, q)

            st.write("Encrypted", en_msg)

        
        if st.button('Decrypt'):
            item = fetch_details(key, 'Elgamal')

            p,p1,q,h = item.get('p'), item.get('p1'), item.get('q'), item.get('h')

            p=int(p)
            p1=int(p1)
            q=int(q)
            h=int(h)
            
            dr_msg = decrypt_by_elgamal(en_msg, p1, key, p)
            dmsg = ''.join(dr_msg)
            st.write("Decrypted Message - ", dmsg)


        data_dict = {"data": en_msg}
    
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

    st.write("Key pushed into server ", details)

    # Check if the length of details is 7, indicating the presence of 'username' and 'filename'
    if len(details) == 8:
        # Check if details with the same username and filename already exist
        existing_data = fetch_existing_data(details[5], details[6])  # Assuming details[5] is 'filename' and details[6] is 'username'
        if existing_data:
            st.warning('Details with the same username and filename already exist')
            return False

    # Construct the data to be pushed
    if len(details) == 8:
        data = {'cipher_name': cipher_name, 'p1': details[0], 'p': details[1], 'h': details[2], 'q': details[3],
                'key': details[4], 'filename': details[5], 'username': details[6], 'en_list' : details[7]}
    else:
        data = {'cipher_name': cipher_name, 'key': details[0], 'n': details[1]}

    # Push the data to the server
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        st.success('Details added successfully')
        return True
    else:
        st.warning('Failed to add details')
        return False

def fetch_existing_data(filename, username):
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



def fetch_details(key, cipher_name):
    url = 'http://127.0.0.1:5000/details'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get('details', [])
        if data:
            for item in data:
                if item.get('key') == key and item.get('name') == cipher_name:
                    st.write('Details found for key', key)
                    return item
            st.warning('No details found for key')
            return None
        else:
            st.warning("No data returned from the server")
            return None
    else:
        print('Failed to fetch details. Status code:', response.status_code)
        return None


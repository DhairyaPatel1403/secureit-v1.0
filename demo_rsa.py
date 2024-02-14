import streamlit as st
import math
import sympy
import io
import bson
import random
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

def rsa(str_msg, p, q, n, e, d):
    st.header("By RSA")

    encr_list = []

    st.warning(f"p, q, n, e, d - {p}, {q}, {n}, {e}, {d}")

    for i in str_msg:
        c = encrypted_by_rsa(ord(i), e, n)
        encr_list.append(c)

    st.write("Encrypted message =", encr_list)

    decry_msg = decryption_by_rsa(encr_list, d, n)
    st.write("Decrypted message =", decry_msg)

    # Convert the list to a dictionary with a specific key
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
        file_name="encrypted_list_rsa.bson",
        mime="application/octet-stream",
    )

    loaded_data_dict = bson.loads(buffer.getvalue())

    # Extract the list from the loaded dictionary
    loaded_encr_list = loaded_data_dict.get("data", [])

    # Display the loaded list (for demonstration purposes)
    st.write("Loaded Encrypted List:")
    st.write(loaded_encr_list)




def is_sophie_germain_prime(p):

    if (sympy.isprime(p) and sympy.isprime((2*p)+1)):
        return True

def encrypt():
    st.write("encrypt")



    # Message to be encrypted (converted to integer)
    encr_list = []
    str_msg = """ """



    #read file

    uploaded_file = st.file_uploader("Choose a file")

    # Check if a file was uploaded
    if uploaded_file is not None:
        try:
            # Read the content of the uploaded file into a string
            str_msg = uploaded_file.read().decode('utf-8')

            # Print or use the string as needed
            st.write("Content of the file:")
            st.write(str_msg)

        except Exception as e:
            st.error(f"Error: {e}")
   
    st.write("Message data =", str_msg)





    p = 61813 # Choose a large prime number
    q = 83983  # Choose another large prime number
    n = p * q
    e =  65537  # Commonly used value for e

    # e = 18908 will give prime key d
    # e = 65537 will give composite key d 
    #not applicable after new p and q
    
    phi = (p - 1) * (q - 1)


    while math.gcd(e, phi) != 1:
        e = sympy.nextprime(e + 1)


    d = modinv(e, phi)

    st.write("Private key is ", d, "e is ", e)



    rsa(str_msg, p, q, n, e, d)



encrypt()
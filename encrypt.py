import streamlit as st
import math
import sympy
import io
import bson
import zipfile


def encrypted(msg, e, n):
    c = pow(msg, e, n)
    return c


def decryption(c, d, n):
    m = pow(c, d, n)
    return chr(m)


def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def encrypt():
    st.write("encrypt")
    p = sympy.nextprime(1000)
    q = sympy.nextprime(2000)
    n = p * q
    e = 65537
    phi = (p - 1) * (q - 1)


    while e < phi:
        if math.gcd(e, phi) == 1:
            break
        else:
            e = e + 1


    d = modinv(e, phi)


    # Get a list of uploaded files
    uploaded_files = st.file_uploader("Choose multiple files", accept_multiple_files=True)


    # Check if any files were uploaded
    if uploaded_files:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for uploaded_file in uploaded_files:
                try:
                    # Read the content of each uploaded file into a string
                    file_content = uploaded_file.read().decode('utf-8')
                    st.write(f"Content of {uploaded_file.name}:")
                    st.write(file_content)


                    # Encrypt the file content
                    encr_list = [encrypted(ord(i), e, n) for i in file_content]


                    # Convert the list to a dictionary with a specific key
                    data_dict = {"data": encr_list}


                    # Convert the dictionary to BSON format
                    bson_data = bson.dumps(data_dict)


                    # Add the encrypted content to the zip file
                    zip_file.writestr(f"encrypted_{uploaded_file.name}.bson", bson_data)


                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {e}")


        # Create a download button for the zip file
        st.download_button(
            label="Download All Encrypted Files",
            key="download_all_files",
            data=zip_buffer.getvalue(),
            file_name="encrypted_files.zip",
            mime="application/zip",
        )

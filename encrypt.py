import streamlit as st
import math
import sympy
import io
import bson


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
    p = sympy.nextprime(1000)  # Choose a large prime number
    q = sympy.nextprime(2000)  # Choose another large prime number
    n = p * q
    e = 65537  # Commonly used value for e
    phi = (p - 1) * (q - 1)


    while e < phi:
        if math.gcd(e, phi) == 1:
            break
        else:
            e = e + 1


    d = modinv(e, phi)


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


    for i in str_msg:
        c = encrypted(ord(i), e, n)
        encr_list.append(c)

    st.write(encr_list)


   
    decry_msg = ""
    for i in encr_list:
        a = decryption(i, d, n)
        decry_msg += a
    st.write(decry_msg)


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
        file_name="encrypted_list.bson",
        mime="application/octet-stream",
    )

    loaded_data_dict = bson.loads(buffer.getvalue())

    # Extract the list from the loaded dictionary
    loaded_encr_list = loaded_data_dict.get("data", [])

    # Display the loaded list (for demonstration purposes)
    st.write("Loaded Encrypted List:")
    st.write(loaded_encr_list)




   
# Call the login function








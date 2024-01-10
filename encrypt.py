
import streamlit as st
import math
import sympy
import io
import bson
import random
from PIL import Image
import base64



def encrypted_by_rsa(msg, d, n):
    c = pow(msg, d, n)
    return c




def decryption_by_rsa(c, e, n):
    m = pow(c, e, n)
    return chr(m)
 




def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1




def rsa(str_msg, encr_list, p, q, n, e, d,file_type):

    st.header("By Rsa")

    for i in str_msg:
        c = encrypted_by_rsa(ord(i), d, n)
        encr_list.append(c)


    st.write(encr_list)

    decry_msg = ""
    for i in encr_list:
        a = decryption_by_rsa(i, e, n)
        decry_msg += a
    st.write("decrypted message =", decry_msg)




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




def power(a, b, c):
    x = 1
    y = a
 
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)
 
    return x % c


def gen_key_e(q):  #generate private key for sender
 
    key = random.randint(0, q)
    while math.gcd(q, key) != 1:
        key = random.randint(0, q)
 
    return key






def encrypt_by_elgamal(msg, q, h, g):
 
    en_msg = []
 
    k = gen_key_e(q) # Private key for sender
    s = power(h, k, q)
    p = power(g, k, q)
     
    for i in range(0, len(msg)):
        en_msg.append(msg[i])
 
    print("g^k used : ", p)
    print("g^ak used : ", s)
    for i in range(0, len(en_msg)):
        en_msg[i] = s * ord(en_msg[i])
 
    return en_msg, p
 
def decrypt_by_elgamal(en_msg, p, key, q):
 
    dr_msg = []
    h = power(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i]/h)))
         
    return dr_msg










def string_to_image(img_str):
    img_data = base64.b64decode(img_str)
    img = Image.open(io.BytesIO(img_data))
    return img






def image_to_string(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str



def elgamal(str_msg, d, q, g,file_type):
    # key exchange using diffie hellman and elgamal algorithm
    st.header("ElGamal")

    key = d #private key for reciver


    h = power(g, key, q)


    print("g used : ", g)
    print("g^a used : ", h)


    en_msg, p = encrypt_by_elgamal(str_msg, q, h, g)
    dr_msg = decrypt_by_elgamal(en_msg, p, key, q)
    dmsg = ''.join(dr_msg)
    
    if file_type in ['jpg', 'jpeg', 'png']:
        st.write("Encrypted Message - ",en_msg)
        reconstructed_img = string_to_image(dmsg)
        st.write("Decrypted Image")
        st.image(reconstructed_img, caption="Reconstructed Image", use_column_width=True)
    else:
      st.write("Encrypted Message - ",en_msg, "Decrypted Message - ", dmsg)

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


def is_sophie_germain_prime(p):


    if (sympy.isprime(p) and sympy.isprime((2*p)+1)):
        return True


def encrypt():
    st.write("encrypt")


    # Message to be encrypted (converted to integer)
    encr_list = []
    str_msg = """ """
    file_type = ""


    #read file

    uploaded_file = st.file_uploader("Choose a file")
    file_type = uploaded_file.name.split(".")[-1].lower()
    # Check if a file was uploaded
    if uploaded_file is not None:
        try:


            if uploaded_file.name.split(".")[-1].lower() in ['jpg', 'jpeg', 'png']:

                file_type = uploaded_file.name.split(".")[-1].lower()
                st.write("Going to image")
                img = Image.open(uploaded_file)
                 # Display the original image
                st.image(img, caption="Original Image", use_column_width=True)
                 # Convert the image to a string
                str_msg = image_to_string(img)


            else:
                file_type = ""
                st.write("Going to text")
                # Read the content of the uploaded file into a string
                str_msg = uploaded_file.read().decode('utf-8')


            # Print or use the string as needed
            st.write("Content of the file:")
            st.write(str_msg)


        except Exception as e:
            st.error(f"Error: {e}")
   
    st.write("Message data =", str_msg)


    p = sympy.nextprime(1000)  # Choose a large prime number
    q = sympy.nextprime(2000)  # Choose another large prime number
    n = p * q
    e = 65537  # Commonly used value for e


    # e = 18908 will give prime key d
    # e = 65537 will give composite key d
   
    phi = (p - 1) * (q - 1)




    while math.gcd(e, phi) != 1:
        e = sympy.nextprime(e + 1)




    d = modinv(e, phi)


    st.write("Private key is ", d)




    if(sympy.isprime(d)):
        rsa(str_msg, encr_list, p, q, n, e, d,file_type)


    else:
        elgamal(str_msg, d, p, q,file_type)



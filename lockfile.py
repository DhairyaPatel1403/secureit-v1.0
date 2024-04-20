import streamlit as st
from elgamal import elgamal 
from rsa import rsa
import math
import sympy




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




def lockfile():
    
    #read file

    str_msg=""

    uploaded_file = st.file_uploader("Choose a file")

    # Check if a file was uploaded
    if uploaded_file is not None:
        try:
            # Read the content of the uploaded file into a string
            str_msg = uploaded_file.read().decode('utf-8')

            # # Print or use the string as needed
            # st.write("Content of the file:")
            # st.write(str_msg)

        except Exception as e:
            st.error(f"Error: {e}")
   
    # st.write("Message data =", str_msg)



    if(uploaded_file):

        p = 10009 # Choose a large prime number
        q = 10007   # Choose another large prime number
        n = p * q
        e =  10000000019   # Commonly used value for e

        # e = 18908 will give prime key d
        # e = 65537 will give composite key d 
        #not applicable after new p and q
        
        phi = (p - 1) * (q - 1)


        while math.gcd(e, phi) != 1:
            e = sympy.nextprime(e + 1)


        d = modinv(e, phi)

        # st.write("Private key is ", d, "e is ", e)

        col13,col14 = st.columns(2)

        if (d < 462580593179):
            rsa(str_msg, d, p, q, e)
        else:
            elgamal(str_msg, d, p, q, e)
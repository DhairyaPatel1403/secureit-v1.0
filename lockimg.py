import streamlit as st
from PIL import Image
import numpy as np
import io
from io import BytesIO
import base64
import zlib
import binascii
from rsa import rsa
from elgamal import elgamal
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



def lockimg():
    st.title("Keep Your images SaFe")
    # File uploader to upload the image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        
        bytes_data = uploaded_image.getvalue()
        # Convert bytes to base64 string
        base64_str = base64.b64encode(bytes_data).decode()
        text_img = base64_str

        # st.write(text_img)



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

        if(d < 462580593179):
            rsa(text_img, d, p, q, e)

        else:
            elgamal(text_img, d, p, q, n)


        



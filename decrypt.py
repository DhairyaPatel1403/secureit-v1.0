import streamlit as st
import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
import requests
from face import detect


def power(a, b, c):
    x = 1
    y = a
    
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)
 
    return x % c


def decrypt_by_elgamal(en_msg, p, key, q):
 
    dr_msg = []
    h = power(p, key, q)
    # st.write("h",h)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i]/h)))
         
    return dr_msg



def submit_form(email, message):
    # Formspree endpoint to handle form submissions
    formspree_endpoint = "https://formspree.io/f/xgegvqaa"

    # Prepare data to send to Formspree
    data = {
        'email': email,
        'message': message,
        # Add other form fields as needed
    }

    # Make a POST request to Formspree
    response = requests.post(formspree_endpoint, data=data)

    # You can handle the response as needed
    if response.status_code == 200:
        st.toast("Warning send to owner")
    else:
        st.warning("Error getting warning to user...")


def main_dec_demo(en_list, p_, key_):

    #en_list = [2921200, 3038048, 2833564, 3067260, 3330168, 3534652, 2833564, 934784, 3271744, 2833564, 3388592, 2950412, 3154896, 934784, 3271744, 2833564, 3359380, 3359380, 3476228, 3242532, 3330168, 2921200, 934784, 2979624, 3242532, 3330168, 934784, 3008836, 3242532, 3242532, 3008836, 3154896, 2950412]
    #dynamic


    #fixed
    q=61813

    on = True

    if on:
        dr_msg = decrypt_by_elgamal(en_list, p_,  key_, q)
        dmsg = ''.join(dr_msg)

        name=""

        if 'face_name' in st.session_state:
            name=st.session_state.face_name

        if name is not None and name!="" and name!="Unknown":

            if name=="Dhairya":
                st.write(dmsg)
            else:
                st.warning("Face Not recognized, [ALARM] 1")

        else:
            st.write("Please upload face.")


    email = st.toggle("Open email services.")

    if email:

        placeholder = st.empty()

        placeholder.message = st.text_input("Enter your message")
        
        if st.button("Send Email"):
            submit_form("dpvp1403@gmail.com", placeholder.message)
            placeholder.empty()
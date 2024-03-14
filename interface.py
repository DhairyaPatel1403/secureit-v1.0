import streamlit as st
import math
import sympy
import io
import bson
import random
from encrypt import encrypt
from fetch import fetch_elgamal
from fetch import fetch_rsa
from decrypt import  main_dec_demo
from face import detect
from decrypt import submit_form
from elgamal import fetch_details

 
def interface(): 


    container1 = st.container(border=True)      
    container2 = st.container(border=True)

    col1, col2 = st.columns(2)

    with col1:
        with container1:
                st.header('Lock a File 🔒')
                encrypt()

    with col2:
        with container2:

                st.header('Unlock a File 🔑')


                st.write('By Default user id is 35') 

                file_name = st.text_input('Enter the name of file.')

                entered_password = st.text_input('Enter the password ...')

                col1, col2 = st.columns(2)

                with col2:
                    key_ = st.text_input("Give personal key")

                if(key_ != ""):
                    key_ = int(key_)

                
                item = fetch_details(key_, 'Elgamal')
                st.write(item)

                p,p1,q,h = item.get('p'), item.get('p1'), item.get('q'), item.get('h')
                
                name = ""

                if(p1 != ""):
                    name = detect()

                

                if st.button('Fetch'):
                    if(entered_password=='' or file_name==''):
                        st.warning('Important fields missing.')
                    else:
                        st.write("p1, key, q", p1, key_, q)
                        if (key_ < 462580593179):
                            decrypted_message = fetch_rsa(35, file_name , entered_password , key_, (p*q))
                        else:
                             decrypted_message = fetch_elgamal(35, file_name , entered_password , p1, key_, p)

                        if name=="Dhairya" or name=="Nirav":
                            st.success(decrypted_message)
                        else:
                            message=f"[USERNAME] tried to access your file {file_name}"
                            submit_form("dpvp1403@gmail.com", message)
                            st.warning("You are NOT authenticated for this activity. Email sent to owner.")
                            
import streamlit as st
import math
import sympy
import io
import bson
import random
from encrypt import encrypt
from fetch import fetch
from decrypt import  main_dec_demo
from face import detect
from decrypt import submit_form
 
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

                p=87
                key=2668142393
                st.write("p, key ", p, key)

                col1, col2 = st.columns(2)

                with col1:
                    p_ = st.text_input("Give p key")
                with col2:
                    key_ = st.text_input("Give personal key")

                if(key_ != ""):
                    key_ = int(key_)

                if(p_ != ""):
                    p_ = int(p_)

                
                name = ""

                if(p_ != ""):
                    #name = detect()
                    name="Dhairya"

                if st.button('Fetch'):
                    if(entered_password=='' or file_name==''):
                        st.warning('Important fields missing.')
                    else:
                        decrypted_message = fetch(35, file_name , entered_password , p_, key_)

                        if name=="Dhairya" or name=="Nirav":
                            st.success(decrypted_message)
                        else:
                            submit_form("dpvp1403@gmail.com", "[USERNAME] tried to access your files." )
                            st.warning("You are NOT authenticated for this activity. Email sent to owner.")
                            
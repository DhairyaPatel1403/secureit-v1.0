import requests
import socket
import streamlit as st 
import pandas as pd
import numpy as np

token="9a0d84d802cd6b"


# hostname = socket.gethostname()
# Addr = socket.gethostbyname(hostname)

def location():
    ip_resp = requests.get("https://api.ipify.org")
    Addr = ip_resp.text

    url = f"https://ipinfo.io/{Addr}?token={token}"

    location=""
    region=""

    response = requests.get(url)
    if response.status_code == 200:
        st.info(Addr)
        st.write(response.json()) 
        location = response.json().get("loc", "Location not found")
        region = response.json().get("region", "Region not found")
    else:
        st.warning(f"Error: Unable to fetch IP information for {Addr}. Status code: {response.status_code}")


    return location,region

# st.map(df)
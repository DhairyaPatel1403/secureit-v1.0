import streamlit as st

def signup():
    with st.form("my_form"):
        st.write("Join with us Today !!")

        name = st.text_input('Your Username')
        password = st.text_input('Your Password (Minimum length - 6 letters)', type='password')
        country = st.text_input('Your Country')

        checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:

            if 'username' not in st.session_state or st.session_state.username=='':
                st.session_state['username'] = name

            st.write(st.session_state.username)

            st.write("slider", "checkbox", checkbox_val)

    st.warning('If already Logged in, log out first to change to other account')
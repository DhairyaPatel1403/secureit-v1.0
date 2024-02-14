import streamlit as st


# Function to render different pages
def render_page(page_name):
    if page_name == 'Login':
        # Import and execute code from page1.py
        from login import login
        login()
    if page_name == 'Signup':
        # Import and execute code from page1.py
        from signup import signup
        signup()
    if page_name == 'Log Out':
        # Import and execute code from page1.py
        from logout import logout
        logout()
    if page_name == 'Main':
        # Import and execute code from page1.py
        from main import main
        main()
    if page_name == 'Encrypt':
        # Import and execute code from page1.py
        from encrypt import encrypt
        encrypt()
    if page_name == 'File':
        # Import and execute code from page1.py
        from push import file
        file()
    if page_name == 'Interface':
        # Import and execute code from page1.py
        from interface import interface
        interface()
    if page_name == 'Decrypt':
        # Import and execute code from page1.py
        from decrypt import main_dec_demo
        main_dec_demo()
    if page_name == 'Face':
        # Import and execute code from page1.py
        from face import main
        main()
    if page_name == 'History':
        # Import and execute code from page1.py
        from history import history
        history()



# Streamlit app
def main():


    st.title(''' Secure:orange[It] ''')

    # Create a navigation bar
    pages = ['Login', 'Signup', 'Log Out', 'Main', 'Encrypt', 'File', 'Interface', 'Decrypt', 'Face', 'History']
    selected_page = st.sidebar.selectbox('Select Page', pages)

    # Render the selected page
    render_page(selected_page)

if __name__ == '__main__':
    
    main()

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



# Streamlit app
def main():
    st.title("SecureIt")

    # Create a navigation bar
    pages = ['Login', 'Signup', 'Log Out', 'Main', 'Encrypt']
    selected_page = st.sidebar.selectbox('Select Page', pages)

    # Render the selected page
    render_page(selected_page)

if __name__ == '__main__':
    main()

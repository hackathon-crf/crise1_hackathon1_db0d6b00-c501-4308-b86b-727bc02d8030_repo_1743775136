import streamlit as st
from pathlib import Path
from frontend.middleware import call_backend_test

def main():
    # Create sidebar buttons
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", ["Default App", "README"])
    
    if selected_page == "Default App":
        st.header("Welcome to the Default ForgeAI Application")
        backend_response = call_backend_test()
        if backend_response:
            st.success(backend_response.get("message"))
            st.write("Data")
            data = backend_response.get("data")
            st.write(data)
        else:
            st.error('Backend is not responding')
            
    else:  # README page
        st.header("Guidelines for Application Automation and Management")
        try:
            readme_path = Path(__file__).parent.parent / "README.md"
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
            st.markdown(readme_content)
        except FileNotFoundError:
            st.error("README.md file not found")
import streamlit as st

def set_style():
    """
    Apply custom styling to the Streamlit app.
    """
    st.markdown("""
    <style>
    .stApp {
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        color: #1E3A8A;
        font-weight: bold;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .emergency-container {
        background-color: #F1F5F9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .warning-banner {
        background-color: #FFEDD5;
        color: #9A3412;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #DC2626;
    }
    </style>
    """, unsafe_allow_html=True)

def generate_top_container(title):
    """
    Generate the top container with app title.
    
    Args:
        title: Application title
    """
    st.markdown(f"<h1 class='main-header'>{title}</h1>", unsafe_allow_html=True)
    st.markdown("---")

def generate_main_container():
    """
    Generate the main application container.
    
    Returns:
        Container object for content
    """
    container = st.container()
    with container:
        st.markdown("<div class='emergency-container'>", unsafe_allow_html=True)
    
    return container
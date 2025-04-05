import streamlit as st
from pathlib import Path
from frontend.middleware import call_backend_test, get_collections, get_emergency_guidance

import streamlit as st
from frontend.components.sidebar import show_sidebar
from frontend.components.collection_selector import render_collection_selector
from frontend.components.emergency_form import render_emergency_form
from frontend.components.response_viewer import render_summary
from frontend.style import set_style, generate_top_container, generate_main_container

# Page configuration
st.set_page_config(
    page_title="FirstRespond AI - Emergency Guidance",
    page_icon="🚑",
    layout="wide"
)

# Initialize session state
if "view" not in st.session_state:
    st.session_state.view = "form"
if "guidance" not in st.session_state:
    st.session_state.guidance = None

# Set custom styles
set_style()

# Generate top container with title
generate_top_container("FirstRespond AI - Emergency First Aid Guidance")


# Show sidebar
show_sidebar()


def main():
    backend_response = call_backend_test()
    if backend_response:
        st.sidebar.success(backend_response.get("message"))
        data = backend_response.get("data")
        #st.write(data)
    else:
        st.error('Backend is not responding')
 
    # Form view
    if st.session_state.get("view", "form") == "form":
        # Instructions
        st.markdown("""
        ### Get emergency guidance using AI-powered first aid knowledge
        
        This application demonstrates how the ForgeAI platform can provide emergency guidance
        by leveraging specialized knowledge collections. Follow these steps:
        
        1. Select relevant knowledge collections below
        2. Fill out the emergency situation form
        3. Review the generated guidance
        
        *Note: This is a demonstration application. In a real emergency, always call emergency services.*
        """)
        
        # Collection selection
        selected_collections = render_collection_selector()
        
        st.divider()
        
        # Emergency form
        form_data = render_emergency_form()
        
        # Process form submission
        if form_data and selected_collections:
            with st.spinner("Generating emergency guidance..."):
                # Get guidance from the backend
                guidance = get_emergency_guidance(form_data, selected_collections)
                #st.write(guidance)
                if guidance:
                    st.session_state.guidance = guidance 
                    render_summary(st.session_state.guidance)
                
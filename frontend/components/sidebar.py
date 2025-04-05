import streamlit as st

def show_sidebar():
    """
    Display the application sidebar.
    """
    with st.sidebar:
        st.title("FirstRespond AI")
        
        st.markdown("### Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.view = "form"
            st.rerun()
        
        
        
        
        st.divider()
        
        st.markdown("### Important Notice")
        st.warning(
            "⚠️ This is a demonstration application. In a real emergency, "
            "always call emergency services first."
        )
        
        st.divider()
        
        st.markdown("### About")
        st.info(
            "FirstRespond AI provides emergency guidance using the ForgeAI "
            "platform's RAG capabilities with specialized first aid knowledge collections."
        )
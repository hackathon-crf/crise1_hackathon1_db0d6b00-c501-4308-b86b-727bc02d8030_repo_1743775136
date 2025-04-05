import streamlit as st
from frontend.middleware import call_backend_test, get_collections


def render_collection_selector():
    """
    Render the collection selection component.
    
    Returns:
        List of selected collections
    """
    try:
        # Fetch available collections
        collections = get_collections()
        
        if not collections or len(collections) == 0:
            st.warning("No collections available in the RAG system. Please ensure collections are loaded.")
            return []
        
        st.subheader("Select Knowledge Collections")
        
        # Simple list approach - works with various data structures
        selected_collections = []
        
        # Handle nested list structure [['guide_pedagogique_psc']]
        if isinstance(collections, list):
            # Flatten the list if it's nested
            flattened_collections = []
            for item in collections:
                if isinstance(item, list):
                    flattened_collections.extend(item)
                else:
                    flattened_collections.append(item)
            
           # Create a single select dropdown for collections
            if flattened_collections:
                selected_collection = st.selectbox(
                    "Select knowledge collection",
                    options=flattened_collections,
                    format_func=str,
                    index=0
                )
                
                # Store the selected collection (as a single item, not a list)
                if selected_collection:
                    selected_collections = selected_collection
                else:
                    selected_collections = None
            else:
                st.warning("No collections available.")
                selected_collections = None
        
        if len(selected_collections) == 0:
            st.info("Please select at least one collection to provide knowledge for the emergency guidance.")
        
        return selected_collections
        
    except Exception as e:
        st.error(f"Error loading collections: {str(e)}")
        return []
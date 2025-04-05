import streamlit as st
import json

def render_summary(guidance):
    """
    Render the emergency guidance summary.
    
    Args:
        guidance: List containing [RAG_extraction, LLM_response]
    """
    if guidance is None:
        st.error("No guidance data available. Please try again.")
        return
    
    rag_extraction = guidance[0]
    llm_response = guidance[1]
    
    # Display the LLM response (guidance)
    if llm_response:
        st.subheader("Emergency Guidance")
        
        # Parse and display JSON response
        if isinstance(llm_response, dict):
            # Summary section
            summary = llm_response.get('summary', 'No summary available')
            st.markdown(f"### Summary\n{summary}")
            
            # Steps section
            steps = llm_response.get('steps', [])
            if steps:
                st.markdown("### Steps to Follow")
                for step in steps:
                    step_num = step.get('step', '')
                    title = step.get('title', '')
                    description = step.get('description', '')
                    st.markdown(f"**Step {step_num}: {title}**")
                    st.markdown(description)
            
            # Checklist section
            checklist = llm_response.get('checklist', [])
            if checklist:
                st.markdown("### Checklist")
                for item in checklist:
                    st.checkbox(item, key=f"check_{item.replace(' ', '_')[:20]}")
            
            # Sources section
            sources = llm_response.get('sources', [])
            if sources:
                st.markdown("### Sources")
                for source in sources:
                    title = source.get('title', 'Unknown source')
                    relevance = source.get('relevance', 'N/A')
                    st.markdown(f"- **{title}** (Relevance: {relevance})")
        else:
            # If not a dict, just display as text
            st.markdown(str(llm_response))
    
    # Display the RAG extraction (source material)
    if rag_extraction:
        with st.expander("View Source Material", expanded=False):
            if isinstance(rag_extraction, list):
                # Handle RAG extraction as a list
                if len(rag_extraction) > 0 and isinstance(rag_extraction[0], list):
                    # This appears to be a list of document sections (based on your example)
                    st.markdown("### Source Passages")
                    for j, section in enumerate(rag_extraction[0]):
                        st.markdown(f"**Passage {j+1}:**")
                        st.markdown(section)
                        st.markdown("---")
                else:
                    # Display each item in the list
                    for i, item in enumerate(rag_extraction):
                        st.markdown(f"**Source {i+1}:**")
                        st.markdown(str(item))
                        st.markdown("---")
            elif isinstance(rag_extraction, dict):
                # Handle structured RAG response
                documents = rag_extraction.get('documents', [])
                if documents:
                    for i, doc in enumerate(documents):
                        st.markdown(f"**Source {i+1}:**")
                        if isinstance(doc, dict):
                            # Extract text and metadata
                            text = doc.get('text', 'No text available')
                            metadata = doc.get('metadata', {})
                            source = metadata.get('source', 'Unknown')
                            
                            st.markdown(f"From: {source}")
                            st.markdown(text)
                        else:
                            st.markdown(str(doc))
                        st.markdown("---")
                else:
                    st.json(rag_extraction)
            else:
                # Display raw response
                st.markdown(str(rag_extraction))
    
    # Handle case where both are None
    if not llm_response and not rag_extraction:
        st.error("Failed to generate emergency guidance. Please try again.")
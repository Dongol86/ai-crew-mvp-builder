import streamlit as st
from main import AICrew
import os
import tempfile
import json

st.set_page_config(page_title="AI Crew MVP Builder", layout="wide")

def main():
    st.title("AI Crew MVP Builder")
    
    # Project Brief Input
    st.header("Project Brief")
    project_brief = st.text_area(
        "Enter your project brief",
        height=200,
        placeholder="Describe your MVP project..."
    )
    
    # File Upload
    st.header("Additional Documents")
    uploaded_files = st.file_uploader(
        "Upload supporting documents",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'pptx']
    )
    
    if 'crew' not in st.session_state:
        st.session_state.crew = None
    
    if st.button("Generate Analysis"):
        if project_brief:
            with st.spinner("AI Crew is analyzing your project..."):
                crew = AICrew()
                st.session_state.crew = crew
                
                # Handle file uploads
                doc_paths = []
                temp_dir = tempfile.mkdtemp()
                try:
                    if uploaded_files:
                        for file in uploaded_files:
                            temp_path = os.path.join(temp_dir, file.name)
                            with open(temp_path, "wb") as f:
                                f.write(file.getvalue())
                            doc_paths.append(temp_path)
                
                    # Process project
                    results = crew.process_project(project_brief, doc_paths if doc_paths else None)
                
                    # Display Results
                    st.header("Project Analysis")
                    if "synthesis" in results:
                        st.markdown(results["synthesis"])
                    elif "error" in results:
                        st.error(results["error"])
                finally:
                    # Cleanup temp files
                    if uploaded_files:
                        for path in doc_paths:
                            if os.path.exists(path):
                                os.remove(path)
                        os.rmdir(temp_dir)
    
    # Follow-up questions section
    if st.session_state.crew is not None:
        st.divider()
        with st.container():
            st.subheader("Ask Follow-up Questions")
            question = st.text_input("What would you like to know more about?")
            if question and st.button("Ask Question"):
                with st.spinner("Processing your question..."):
                    answer = st.session_state.crew.ask_followup(question)
                    st.markdown(answer)

if __name__ == "__main__":
    main()
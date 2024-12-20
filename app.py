import streamlit as st
from main import AICrew
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
    
    if st.button("Generate Analysis"):
        if project_brief:
            with st.spinner("AI Crew is analyzing your project..."):
                crew = AICrew()
                results = crew.process_project(project_brief, uploaded_files)
                
                # Display Results
                st.header("Analysis Results")
                tabs = st.tabs([
                    "Strategic Lead",
                    "Growth Strategy",
                    "UX Design",
                    "Technical Architecture",
                    "DevOps"
                ])
                
                for tab, (agent, output) in zip(tabs, results.items()):
                    with tab:
                        st.markdown(f"### {agent.replace('_', ' ').title()}")
                        st.write(output)

if __name__ == "__main__":
    main()
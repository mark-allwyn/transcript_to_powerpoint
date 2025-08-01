"""
Test app to verify imports work
"""

import streamlit as st
import sys
import importlib.util
from pathlib import Path

st.title("Import Test")

# Test OpenAI import
if st.button("Test OpenAI Import"):
    try:
        # Load OpenAI app module directly
        openai_app_path = Path(__file__).parent / "openai" / "app.py"
        spec = importlib.util.spec_from_file_location("openai_app", openai_app_path)
        openai_app = importlib.util.module_from_spec(spec)
        
        # Add openai directory to path temporarily
        openai_path = str(Path(__file__).parent / "openai")
        if openai_path not in sys.path:
            sys.path.insert(0, openai_path)
        
        try:
            spec.loader.exec_module(openai_app)
            
            # Get the functions we need
            generate_slide_package = openai_app.generate_slide_package
            simple_slide_generation = openai_app.simple_slide_generation
            build_pptx = openai_app.build_pptx
            
            st.success("✅ OpenAI imports successful!")
            st.write(f"generate_slide_package: {callable(generate_slide_package)}")
            st.write(f"simple_slide_generation: {callable(simple_slide_generation)}")
            st.write(f"build_pptx: {callable(build_pptx)}")
            
        finally:
            # Clean up path
            if openai_path in sys.path:
                sys.path.remove(openai_path)
                
    except Exception as e:
        st.error(f"❌ OpenAI import failed: {str(e)}")

# Test CrewAI import
if st.button("Test CrewAI Import"):
    try:
        # Load CrewAI app module directly
        crewai_app_path = Path(__file__).parent / "crewai" / "app.py"
        spec = importlib.util.spec_from_file_location("crewai_app", crewai_app_path)
        crewai_app = importlib.util.module_from_spec(spec)
        
        # Add crewai directory to path temporarily
        crewai_path = str(Path(__file__).parent / "crewai")
        if crewai_path not in sys.path:
            sys.path.insert(0, crewai_path)
            
        try:
            spec.loader.exec_module(crewai_app)
            
            # Get the function we need
            process_transcript_with_crewai = crewai_app.process_transcript_with_crewai
            
            st.success("✅ CrewAI imports successful!")
            st.write(f"process_transcript_with_crewai: {callable(process_transcript_with_crewai)}")
            
        finally:
            # Clean up path
            if crewai_path in sys.path:
                sys.path.remove(crewai_path)
                
    except Exception as e:
        st.error(f"❌ CrewAI import failed: {str(e)}")
        st.info("This is expected if CrewAI dependencies are not installed in the main environment")

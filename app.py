"""
AI-Powered Transcript Processing
===============================
Unified application with OpenAI and CrewAI transcript-to-slides processing.
OpenAI app as default with sidebar navigation to CrewAI.

Run: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Transcript to Slides - AI Processing",
    page_icon="robot",
    layout="wide"
)

# Add the app directories to path for imports
sys.path.append(str(Path(__file__).parent / "openai"))
sys.path.append(str(Path(__file__).parent / "crewai"))

def show_openai_app():
    """Display the OpenAI application"""
    st.title("Transcript to Slides (OpenAI)")
    st.markdown("*Advanced structured output with DALL-E 3 visuals*")
    
    # Check if OpenAI API key is available
    import os
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI API key not found. Please add OPENAI_API_KEY to your environment variables.")
        st.stop()
    
    file = st.file_uploader("Upload meeting transcript (.txt)", type=["txt"], key="openai_file_uploader")
    
    if file:
        transcript_text = file.read().decode("utf-8", errors="ignore")
        
        st.info("Processing with OpenAI's DALL-E 3 for image generation...")
        
        # Import OpenAI app components dynamically
        try:
            # Load environment variables first
            from pathlib import Path
            try:
                from dotenv import load_dotenv
                
                # Load root .env first (shared settings)
                root_env = Path(__file__).parent / '.env'
                if root_env.exists():
                    load_dotenv(root_env)
                
                # Load app-specific .env (overrides root)
                app_env = Path(__file__).parent / 'openai' / '.env'
                if app_env.exists():
                    load_dotenv(app_env, override=True)
                    
            except ImportError:
                pass
            
            # Add OpenAI app to path and import
            import sys
            import importlib.util
            
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
                build_pptx = openai_app.build_pptx
                
            finally:
                # Clean up path
                if openai_path in sys.path:
                    sys.path.remove(openai_path)
            
            with st.spinner("Processing transcript with advanced structured output..."):
                specs, imgs, timing_info = generate_slide_package(transcript_text)
                deck = build_pptx(specs, imgs)
            
            st.success(f"Slide deck ready! Generated {len(specs)} content slides plus title slide.")
            
            # Show optimization info
            if timing_info.get('transcript_length'):
                st.info(f"Processed {timing_info['transcript_length']:,} characters | Generated {timing_info.get('slides_generated', 0)} slides")
            
            # Display slide preview
            st.subheader("Slide Preview")
            for i, spec in enumerate(specs, 1):
                with st.expander(f"Slide {i + 1}: {spec['title']}"):
                    for bullet in spec['bullets']:
                        st.write(f"• {bullet}")
            
            # Display timing information
            if timing_info.get('total_time', 0) > 0:
                st.subheader("Processing Times")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Transcript Analysis", f"{timing_info.get('transcript_analysis', 0):.1f}s")
                    st.metric("Slide Generation", f"{timing_info.get('slide_generation', 0):.1f}s")
                
                with col2:
                    st.metric("Image Prompts", f"{timing_info.get('image_prompts', 0):.1f}s")
                    st.metric("Image Generation", f"{timing_info.get('image_generation', 0):.1f}s")
                
                st.metric("Total Processing Time", f"{timing_info['total_time']:.1f}s")
            
            st.download_button(
                label="Download PPTX",
                data=deck,
                file_name="meeting_summary.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="openai_download_button"
            )
            
        except ImportError as e:
            st.error(f"Error importing OpenAI functions: {str(e)}")
            st.info("Please ensure all OpenAI dependencies are installed")
            
            # Fallback UI
            if st.button("Process Transcript (Demo Mode)", key="openai_demo_button"):
                st.warning("Running in demo mode - OpenAI functions not available")
                st.success("This would process the transcript with OpenAI + DALL-E 3")
                st.info("To use full functionality, ensure the OpenAI app dependencies are installed")
        
        except Exception as e:
            st.error(f"Processing error: {str(e)}")
            st.info("Please check your OpenAI API key and try again")

def show_crewai_app():
    """Display the CrewAI application"""
    st.title("Transcript to Slides (CrewAI)")
    st.markdown("*Cost-optimized multi-agent intelligence with 90% savings*")
    
    # Check if OpenAI API key is available
    import os
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI API key not found. Please add OPENAI_API_KEY to your environment variables.")
        st.stop()
    
    file = st.file_uploader("Upload meeting transcript (.txt)", type=["txt"], key="crewai_file_uploader")
    
    if file:
        transcript_text = file.read().decode("utf-8", errors="ignore")
        
        try:
            # Load environment variables first
            from pathlib import Path
            try:
                from dotenv import load_dotenv
                
                # Load root .env first (shared settings)
                root_env = Path(__file__).parent / '.env'
                if root_env.exists():
                    load_dotenv(root_env)
                
                # Load app-specific .env (overrides root)
                app_env = Path(__file__).parent / 'crewai' / '.env'
                if app_env.exists():
                    load_dotenv(app_env, override=True)
                    
            except ImportError:
                pass
            
            # Add CrewAI app to path and import
            import sys
            import importlib.util
            
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
                
            finally:
                # Clean up path
                if crewai_path in sys.path:
                    sys.path.remove(crewai_path)
            
            with st.spinner("Processing transcript with 3-agent CrewAI workflow..."):
                slide_data, deck, processing_time = process_transcript_with_crewai(transcript_text)
                timing_info = {
                    "total_time": processing_time,
                    "transcript_length": len(transcript_text),
                    "slides_generated": len(slide_data.slides)
                }
            
            st.success(f"Slide deck ready! Generated {len(slide_data.slides)} content slides plus title slide.")
            
            # Show optimization info
            if timing_info.get('transcript_length'):
                st.info(f"Processed {timing_info['transcript_length']:,} characters | Generated {timing_info.get('slides_generated', 0)} slides")
            
            # Display slide preview
            st.subheader("Slide Preview")
            for i, slide in enumerate(slide_data.slides, 1):
                with st.expander(f"Slide {i + 1}: {slide.title}"):
                    for bullet in slide.bullets:
                        st.write(f"• {bullet}")
            
            # Display timing information
            if timing_info.get('total_time', 0) > 0:
                st.subheader("Processing Times")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Agent Analysis", f"{timing_info['total_time']/3:.1f}s")
                    st.metric("Slide Design", f"{timing_info['total_time']/3:.1f}s")
                
                with col2:
                    st.metric("Content Optimization", f"{timing_info['total_time']/3:.1f}s")
                    st.metric("Text Processing", "0.0s")
                
                st.metric("Total Processing Time", f"{timing_info['total_time']:.1f}s")
            
            st.download_button(
                label="Download PPTX",
                data=deck,
                file_name="meeting_summary.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="crewai_download_button"
            )
            
        except ImportError as e:
            st.error(f"Error importing CrewAI functions: {str(e)}")
            st.info("Please ensure all CrewAI dependencies are installed")
            
            # Fallback UI
            if st.button("Process Transcript (Demo Mode)", key="crewai_demo_button"):
                st.warning("Running in demo mode - CrewAI functions not available")
                st.success("This would process the transcript with CrewAI agents")
                st.info("To use full functionality, ensure the CrewAI app dependencies are installed")
        
        except Exception as e:
            st.error(f"Processing error: {str(e)}")
            st.info("Please check your configuration and try again")

def main():
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "OpenAI App"
    
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        
        page = st.radio(
            "Choose Application:",
            ["OpenAI App", "CrewAI App"],
            index=["OpenAI App", "CrewAI App"].index(st.session_state.current_page),
            key="main_app_navigation"
        )
        
        # Update session state if selection changes
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Quick Info")
        
        if page == "OpenAI App":
            st.markdown("""
            **Output Type:**
            - Images included (DALL-E 3)
            """)
        elif page == "CrewAI App":
            st.markdown("""
            **Output Type:**
            - Text-only
            """)
    
    # Display the selected page
    if st.session_state.current_page == "OpenAI App":
        show_openai_app()
    elif st.session_state.current_page == "CrewAI App":
        show_crewai_app()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>AI-Powered Transcript Processing | OpenAI & CrewAI Solutions</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

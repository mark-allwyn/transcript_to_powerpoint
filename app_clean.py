"""
AI-Powered Document Processing Suite
===================================
Unified application providing access to multiple AI-powered transcript processing tools.
All apps accessible through a single interface on one port.

Run: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="AI Document Processing Suite",
    page_icon="robot",
    layout="wide"
)

# Add the app directories to path for imports
sys.path.append(str(Path(__file__).parent / "openai"))
sys.path.append(str(Path(__file__).parent / "crewai"))

def show_hub():
    """Display the main hub page"""
    st.title("AI-Powered Document Processing Suite")
    st.markdown("---")
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to the AI Document Processing Suite
        
        Choose from our collection of AI-powered applications for converting meeting transcripts 
        into professional PowerPoint presentations. Each app offers different capabilities and 
        optimization strategies.
        """)
        
        st.info("Pro Tip: For cost-sensitive deployments, we recommend the CrewAI app which offers 90% cost reduction while maintaining professional quality.")
    
    with col2:
        st.markdown("### Quick Stats")
        st.metric("Available Apps", "2")
        st.metric("Supported Formats", "TXT")
        st.metric("Output Format", "PPTX")
    
    st.markdown("---")
    
    # Application Grid
    st.subheader("Available Applications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### OpenAI Transcript to Slides")
        st.markdown("""
        **Premium AI-powered presentations with visuals**
        
        **Features:**
        - GPT-4o-mini smart analysis
        - DALL-E 3 image generation
        - Rich visual presentations
        - Performance metrics
        
        **Best for:**
        - High-impact presentations
        - Visual storytelling
        - Client-facing materials
        """)
        
        if st.button("Launch OpenAI App", key="nav_openai", use_container_width=True):
            st.session_state.current_page = "OpenAI App"
            st.rerun()
    
    with col2:
        st.markdown("### CrewAI Transcript to Slides")
        st.markdown("""
        **Cost-optimized multi-agent intelligence**
        
        **Features:**
        - 3-agent collaborative workflow
        - 90% cost reduction
        - Text-only efficiency
        - Professional output
        
        **Best for:**
        - Cost-sensitive deployments
        - High-volume processing
        - Internal documentation
        """)
        
        if st.button("Launch CrewAI App", key="nav_crewai", use_container_width=True):
            st.session_state.current_page = "CrewAI App"
            st.rerun()
    
    st.markdown("---")
    
    # Comparison Table
    st.subheader("Application Comparison")
    
    comparison_data = {
        "Feature": [
            "AI Model",
            "Image Generation",
            "Cost Efficiency",
            "Processing Speed",
            "Output Quality",
            "Best Use Case"
        ],
        "OpenAI App": [
            "GPT-4o-mini",
            "Yes (DALL-E 3)",
            "Standard",
            "Fast",
            "Premium",
            "Client presentations"
        ],
        "CrewAI App": [
            "GPT-4o-mini (3 agents)",
            "No (Text-only)",
            "90% savings",
            "Fast",
            "Professional",
            "Internal docs"
        ]
    }
    
    st.table(comparison_data)

def show_openai_app():
    """Display the OpenAI application"""
    st.title("Transcript to Slides (OpenAI)")
    st.markdown("*Premium AI-powered presentations with DALL-E 3 visuals*")
    
    # Check if OpenAI API key is available
    import os
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI API key not found. Please add OPENAI_API_KEY to your environment variables.")
        st.stop()
    
    # Add generation method selector
    generation_method = st.radio(
        "Choose generation method:",
        ["Advanced (Structured Output)", "Simple (Backup Method)"],
        index=0
    )
    
    file = st.file_uploader("Upload meeting transcript (.txt)", type=["txt"])
    
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
            openai_path = str(Path(__file__).parent / "openai")
            if openai_path not in sys.path:
                sys.path.insert(0, openai_path)
            
            # Import specific functions
            from app import generate_slide_package, simple_slide_generation, build_pptx
            
            if generation_method == "Simple (Backup Method)":
                with st.spinner("Processing transcript with simple method..."):
                    specs, imgs = simple_slide_generation(transcript_text)
                    deck = build_pptx(specs, imgs)
                timing_info = {"total_time": 0}
            else:
                with st.spinner("Processing transcript with advanced method..."):
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
            )
            
        except ImportError as e:
            st.error(f"Error importing OpenAI functions: {str(e)}")
            st.info("Please ensure all OpenAI dependencies are installed")
            
            # Fallback UI
            if st.button("Process Transcript (Demo Mode)"):
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
    
    file = st.file_uploader("Upload meeting transcript (.txt)", type=["txt"])
    
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
            crewai_path = str(Path(__file__).parent / "crewai")
            if crewai_path not in sys.path:
                sys.path.insert(0, crewai_path)
            
            # Import the processing function
            from app import process_transcript_with_crewai
            
            with st.spinner("Processing transcript with 3-agent CrewAI workflow..."):
                slide_data, deck, processing_time = process_transcript_with_crewai(transcript_text)
                timing_info = {"total_time": processing_time}
            
            st.success(f"Slide deck ready! Generated {len(slide_data.slides)} content slides plus title slide.")
            
            # Show optimization info
            st.info(f"Processed {len(transcript_text):,} characters | Generated {len(slide_data.slides)} slides")
            
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
            )
            
        except ImportError as e:
            st.error(f"Error importing CrewAI functions: {str(e)}")
            st.info("Please ensure all CrewAI dependencies are installed")
            
            # Fallback UI
            if st.button("Process Transcript (Demo Mode)"):
                st.warning("Running in demo mode - CrewAI functions not available")
                st.success("This would process the transcript with CrewAI agents")
                st.info("To use full functionality, ensure the CrewAI app dependencies are installed")
        
        except Exception as e:
            st.error(f"Processing error: {str(e)}")
            st.info("Please check your configuration and try again")

def main():
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Hub"
    
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        
        page = st.radio(
            "Choose Application:",
            ["Hub", "OpenAI App", "CrewAI App"],
            index=["Hub", "OpenAI App", "CrewAI App"].index(st.session_state.current_page)
        )
        
        # Update session state if selection changes
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Quick Info")
        
        if page == "OpenAI App":
            st.markdown("""
            **Premium Features:**
            - DALL-E 3 images
            - Rich visuals
            - Client-ready
            """)
        elif page == "CrewAI App":
            st.markdown("""
            **Cost-Optimized:**
            - 90% cost savings
            - 3-agent workflow
            - Text-only efficiency
            """)
        else:
            st.markdown("""
            **Hub Features:**
            - App comparison
            - Easy navigation
            - Deployment guide
            """)
    
    # Display the selected page
    if st.session_state.current_page == "Hub":
        show_hub()
    elif st.session_state.current_page == "OpenAI App":
        show_openai_app()
    elif st.session_state.current_page == "CrewAI App":
        show_crewai_app()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>AI-Powered Document Processing Suite | Single-Port Multi-App Interface</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

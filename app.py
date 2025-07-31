"""
Transcript → Slide Deck (with GPT-Image-1 visuals)
--------------------------------------------------
Run:  streamlit run app.py
"""

import os, json, math, textwrap, requests, re, base64
from io import BytesIO
from typing import List
import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pydantic import BaseModel, Field
import openai

# ---------------------------------------------------------------------------
# 0  API key
# ---------------------------------------------------------------------------
openai.api_key = (
    os.getenv("OPENAI_API_KEY")
)

# ---------------------------------------------------------------------------
# 0.5  Pydantic Models for Structured Output
# ---------------------------------------------------------------------------
class MeetingSummary(BaseModel):
    """Structured output for meeting transcript summary"""
    key_points: List[str] = Field(description="List of 3-7 important discussion points from the meeting")
    decisions: List[str] = Field(description="List of decisions made during the meeting", default=[])
    action_items: List[str] = Field(description="List of action items identified", default=[])

class SlideSpec(BaseModel):
    """Specification for a single slide"""
    title: str = Field(description="Slide title, max 8 words, present tense")
    bullets: List[str] = Field(description="3-6 concise bullet points, each under 80 characters")

class SlideSpecs(BaseModel):
    """Collection of slide specifications"""
    slides: List[SlideSpec] = Field(description="Array of slide specifications")

class ImagePrompts(BaseModel):
    """Collection of image generation prompts"""
    prompts: List[str] = Field(description="Array of DALL-E prompts, one for each slide")

# ---------------------------------------------------------------------------
# 1  Helper functions
# ---------------------------------------------------------------------------
def chunk_text(text: str, words_per_chunk: int = 8_000) -> list[str]:
    """Split very long transcripts into ~8 000-word chunks for gpt-3.5."""
    words = text.split()
    if len(words) <= words_per_chunk:
        return [text]
    n_chunks = math.ceil(len(words) / words_per_chunk)
    return [
        " ".join(words[i::n_chunks])  # interleaved ensures similar lengths
        for i in range(n_chunks)
    ]


def merge_summaries(parts: list[dict]) -> dict:
    merged = {"key_points": [], "decisions": [], "action_items": []}
    for p in parts:
        for k in merged:
            merged[k].extend(p.get(k, []))
    return merged


def create_placeholder_image() -> bytes:
    """Create a simple white placeholder image instead of transparent."""
    try:
        from PIL import Image
        # Create a 1024x1024 white image
        img = Image.new('RGB', (1024, 1024), 'white')
        buf = BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    except ImportError:
        # Fallback to a simple base64 encoded white image if PIL not available
        # This is a small white 100x100 PNG image
        white_image_b64 = """
        iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAGklEQVQYV2P4//8/AzYwOjraMDo6
        2jA6OtoAALvMBONcfOGOAAAAAElFTkSuQmCC
        """
        return base64.b64decode(white_image_b64.replace('\n', '').replace(' ', ''))


def create_images_gpt(prompts: list[str]) -> list[bytes]:
    """Generate one image per prompt with DALL-E 3 and return raw bytes."""
    bins = []
    for prompt in prompts:
        try:
            # Use DALL-E 3 for faster and more reliable image generation
            resp = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="standard",  # Valid options are "standard" and "hd"
            )
            url = resp.data[0].url
            if url:
                image_data = requests.get(url, timeout=30).content
                bins.append(image_data)
                print(f"Successfully generated image for prompt: {prompt[:50]}...")
            else:
                print(f"Warning: No URL returned for prompt: {prompt}")
                bins.append(create_placeholder_image())
        except Exception as e:
            print(f"Error generating image for prompt '{prompt[:50]}...': {e}")
            bins.append(create_placeholder_image())
    return bins


def build_pptx(slide_specs: list[dict], images: list[bytes]) -> BytesIO:
    prs = Presentation()
    # Title slide
    tslide = prs.slides.add_slide(prs.slide_layouts[0])
    tslide.shapes.title.text = "Meeting Summary"
    tslide.placeholders[1].text = "AI-generated deck"

    bullet_layout = prs.slide_layouts[1]
    for spec, img_bytes in zip(slide_specs, images):
        sld = prs.slides.add_slide(bullet_layout)
        sld.shapes.title.text = spec["title"]

        body = sld.shapes.placeholders[1].text_frame
        body.clear()  # remove default text
        for bullet in spec["bullets"]:
            p = body.add_paragraph()
            p.text = bullet
            p.level = 0
            p.font.size = Pt(18)

        # insert picture on right side
        pic_stream = BytesIO(img_bytes)
        sld.shapes.add_picture(pic_stream, Inches(5.5), Inches(1.3), width=Inches(3))

    buf = BytesIO()
    prs.save(buf)
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# 3  End-to-end pipeline
# ---------------------------------------------------------------------------

def generate_slide_package(transcript: str):
    # Use direct OpenAI calls with structured output for more reliable results
    from openai import OpenAI
    client = OpenAI()
    
    # 3a  Summarise using OpenAI structured output
    try:
        summary_response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert meeting transcript analyzer. Extract key information from meeting transcripts accurately and completely."
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyze this meeting transcript and extract key information.
                    
                    Extract only what was actually discussed in the meeting:
                    - Key discussion points (3-7 most important items)
                    - Decisions made during the meeting (actual decisions)
                    - Action items identified (specific tasks mentioned)
                    
                    Meeting transcript:
                    {transcript}
                    """
                }
            ],
            response_format=MeetingSummary
        )
        summary_json = summary_response.choices[0].message.parsed.model_dump()
        print(f"DEBUG - OpenAI summary: {summary_json}")
    except Exception as e:
        print(f"DEBUG - OpenAI structured output failed: {e}")
        # Fallback to manual parsing
        summary_json = {"key_points": ["Meeting analysis failed"], "decisions": [], "action_items": []}

    # 3b  Create slides using OpenAI structured output
    try:
        slides_response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a presentation expert who creates slide specifications based on meeting content."
                },
                {
                    "role": "user",
                    "content": f"""
                    Create slide specifications based on this meeting summary.
                    
                    MEETING SUMMARY:
                    {json.dumps(summary_json, indent=2)}
                    
                    Requirements:
                    - Create slides specific to this meeting content
                    - Titles max 8 words, present tense
                    - 3-6 bullet points per slide, each under 80 characters
                    - Use the actual meeting information provided
                    - Professional business presentation style
                    
                    Create slides covering key points, decisions, and action items from the meeting.
                    """
                }
            ],
            response_format=SlideSpecs
        )
        slide_specs = slides_response.choices[0].message.parsed.slides
        slide_specs_data = [spec.model_dump() for spec in slide_specs]
        print(f"DEBUG - Generated {len(slide_specs_data)} slides from OpenAI")
    except Exception as e:
        print(f"DEBUG - OpenAI slides generation failed: {e}")
        # Fallback: Create slides directly from summary
        slide_specs_data = []
        if summary_json.get('key_points'):
            slide_specs_data.append({
                "title": "Key Discussion Points",
                "bullets": summary_json['key_points'][:6]
            })
        if summary_json.get('decisions'):
            slide_specs_data.append({
                "title": "Decisions Made", 
                "bullets": summary_json['decisions'][:6]
            })
        if summary_json.get('action_items'):
            slide_specs_data.append({
                "title": "Action Items",
                "bullets": summary_json['action_items'][:6]
            })
        
        if not slide_specs_data:
            slide_specs_data = [{"title": "Meeting Summary", "bullets": ["Content not available"]}]

    # 3c  Generate image prompts using OpenAI structured output
    try:
        prompts_response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a visual design expert who creates DALL-E prompts for business presentations."
                },
                {
                    "role": "user",
                    "content": f"""
                    Create DALL-E image prompts for these slides based on the meeting content.
                    
                    MEETING CONTEXT:
                    {json.dumps(summary_json, indent=2)}
                    
                    SLIDES TO CREATE IMAGES FOR:
                    {json.dumps(slide_specs_data, indent=2)}
                    
                    Requirements:
                    - Create professional business illustrations
                    - Modern vector-style graphics in blue/gray/white colors
                    - Relevant to the specific meeting content and slide topics
                    - ABSOLUTELY NO TEXT, WORDS, LETTERS, OR NUMBERS in images
                    - Minimalist, clean design
                    - End each prompt with ", no text, no words, no labels"
                    
                    Create one detailed prompt per slide that relates to the actual meeting topics.
                    """
                }
            ],
            response_format=ImagePrompts
        )
        prompts = prompts_response.choices[0].message.parsed.prompts
        print(f"DEBUG - Generated {len(prompts)} image prompts")
    except Exception as e:
        print(f"DEBUG - OpenAI image prompts failed: {e}")
        prompts = [f"Minimalist business illustration for slide {i+1}, no text, no words, no labels" for i in range(len(slide_specs_data))]

    if len(prompts) != len(slide_specs_data):
        print(f"DEBUG - Prompt/slide mismatch: {len(prompts)} prompts vs {len(slide_specs_data)} slides")
        # Adjust prompts to match slides
        if len(prompts) < len(slide_specs_data):
            prompts.extend([f"Business illustration, no text" for _ in range(len(slide_specs_data) - len(prompts))])
        else:
            prompts = prompts[:len(slide_specs_data)]

    # 3d  Image generation
    image_bins = create_images_gpt(prompts)

    return slide_specs_data, image_bins


# ---------------------------------------------------------------------------
# 4  Streamlit UI
# ---------------------------------------------------------------------------
st.title("Transcript → Slides")
file = st.file_uploader("Upload meeting transcript (.txt)", type=["txt"])

if file:
    transcript_text = file.read().decode("utf-8", errors="ignore")
    with st.spinner("Processing transcript…"):
        specs, imgs = generate_slide_package(transcript_text)
        deck = build_pptx(specs, imgs)
    st.success("Slide deck ready!")
    st.download_button(
        label="Download PPTX",
        data=deck,
        file_name="meeting_summary.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )

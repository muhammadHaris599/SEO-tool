"""
Streamlit Dashboard for SEO Content Tool.
Provides a user-friendly interface for content generation and WordPress publishing.
"""

import streamlit as st
import requests
import json
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL = """)

# Page configuration
st.set_page_config(
    page_title="SEO Content Tool",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "topics" not in st.session_state:
        st.session_state.topics = []
    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = None
    if "outline" not in st.session_state:
        st.session_state.outline = None
    if "content" not in st.session_state:
        st.session_state.content = None
    if "current_step" not in st.session_state:
        st.session_state.current_step = "input"


import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def make_api_request(endpoint, method="POST", data=None):
    try:
        if endpoint == "generate-topics":
            prompt = f"Generate 10 SEO blog topics for niche: {data['niche']} with keyword: {data['primary_keyword']}"
        
        elif endpoint == "generate-outline":
            prompt = f"Create a detailed blog outline for topic: {data['topic']}"
        
        elif endpoint == "generate-content":
            prompt = f"Write a full SEO optimized article on: {data['topic']}"
        
        else:
            return {}

        from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)

text = response.choices[0].message.content

        return {
            "topics": [text] if endpoint == "generate-topics" else [],
            "outline": [{"heading": text, "level": 1}],
            "content": {
                "html": text,
                "meta_title": "Generated Title",
                "meta_description": "Generated Description",
                "word_count": len(text.split())
            },
            "status": "success"
        }

    except Exception as e:
        raise Exception(str(e))


def render_header():
    """Render application header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📝 SEO Content Automation Tool")
        st.markdown("Powered by OpenAI GPT-4 & FastAPI")
    with col2:
        if st.button("🔄 Reset", key="reset_btn"):
            st.session_state.current_step = "input"
            st.session_state.topics = []
            st.session_state.selected_topic = None
            st.session_state.outline = None
            st.session_state.content = None
            st.rerun()


def render_input_section():
    """Render user input section."""
    st.header("Step 1: Define Your Content")
    
    col1, col2 = st.columns(2)
    
    with col1:
        niche = st.text_input(
            "Niche/Industry",
            placeholder="e.g., Digital Marketing, SaaS, E-commerce",
            help="The industry or topic area you want to create content for"
        )
        
        keyword = st.text_input(
            "Primary Keyword",
            placeholder="e.g., Best SEO Tools 2024",
            help="The main keyword you want to rank for"
        )
        
        word_count = st.slider(
            "Target Word Count",
            min_value=500,
            max_value=5000,
            value=2000,
            step=100,
            help="Approximate word count for the article"
        )
    
    with col2:
        audience = st.text_area(
            "Target Audience",
            placeholder="e.g., Small business owners, marketing professionals, beginners",
            height=80,
            help="Description of your target audience"
        )
        
        tone = st.selectbox(
            "Writing Tone",
            ["Professional", "Casual", "Friendly", "Authoritative", "Educational"],
            help="The tone and style of the content"
        )
    
    # Topics generation button
    if st.button("🎯 Generate Topics", use_container_width=True, key="generate_topics_btn"):
        if not niche or not keyword:
            st.error("Please fill in Niche and Primary Keyword")
        else:
            with st.spinner("Generating SEO-optimized topics..."):
                try:
                    payload = {
                        "niche": niche,
                        "primary_keyword": keyword,
                        "target_audience": audience,
                        "tone": tone.lower()
                    }
                    
                    result = make_api_request("generate-topics", data=payload)
                    
                    st.session_state.topics = result.get("topics", [])
                    st.session_state.selected_topic = None
                    st.session_state.outline = None
                    st.session_state.content = None
                    st.session_state.current_step = "topics_generated"
                    
                    st.success(f"✅ Generated {len(st.session_state.topics)} topics!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error generating topics: {str(e)}")


def render_topics_section():
    """Render topics selection section."""
    st.header("Step 2: Select Topic")
    st.markdown(f"**Generated {len(st.session_state.topics)} topics:**")
    
    # Display topics in columns
    cols = st.columns(1)
    
    selected_index = None
    for idx, topic in enumerate(st.session_state.topics):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{idx + 1}. {topic}**")
        with col2:
            if st.button("Select", key=f"select_topic_{idx}"):
                selected_index = idx
                st.session_state.selected_topic = topic
                st.session_state.outline = None
                st.session_state.content = None
                st.session_state.current_step = "topic_selected"
                st.rerun()


def render_outline_section():
    """Render outline generation and display."""
    st.header("Step 3: Generate Outline")
    
    topic = st.session_state.selected_topic
    st.info(f"📋 Selected Topic: **{topic}**")
    
    # Get keyword from user input (stored in sidebar or retrieve from first request)
    keyword = st.text_input(
        "Primary Keyword",
        key="outline_keyword",
        placeholder="Enter the main keyword for SEO"
    )
    
    if st.button("📑 Generate Outline", use_container_width=True, key="generate_outline_btn"):
        if not keyword:
            st.error("Please enter the primary keyword")
        else:
            with st.spinner("Generating content outline..."):
                try:
                    payload = {
                        "topic": topic,
                        "primary_keyword": keyword,
                        "target_audience": ""
                    }
                    
                    result = make_api_request("generate-outline", data=payload)
                    
                    st.session_state.outline = result
                    st.session_state.current_step = "outline_generated"
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error generating outline: {str(e)}")
    
    # Display existing outline if available
    if st.session_state.outline:
        st.subheader("Generated Outline")
        
        outline = st.session_state.outline.get("outline", [])
        for section in outline:
            level = section.get("level", 1)
            heading = section.get("heading", "")
            indent = "  " * (level - 1)
            st.write(f"{indent}{'#' * level} {heading}")
        
        st.subheader("FAQ Questions")
        faq = st.session_state.outline.get("faq_questions", [])
        for i, question in enumerate(faq, 1):
            st.write(f"{i}. {question}")


def render_content_section():
    """Render content generation and display."""
    st.header("Step 4: Generate Content")
    
    if not st.session_state.outline:
        st.warning("Please generate an outline first")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        word_count = st.slider(
            "Word Count",
            min_value=500,
            max_value=5000,
            value=2000,
            step=100,
            key="content_word_count"
        )
    
    with col2:
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Friendly", "Authoritative", "Educational"],
            key="content_tone"
        )
    
    if st.button("✍️ Generate Full Content", use_container_width=True, key="generate_content_btn"):
        with st.spinner("Generating full article (this may take a minute)..."):
            try:
                outline_data = st.session_state.outline.get("outline", [])
                payload = {
                    "topic": st.session_state.selected_topic,
                    "primary_keyword": st.session_state.outline.get("faq_questions", [""])[0] if st.session_state.outline else "",
                    "outline": [
                        {
                            "heading": section.get("heading", ""),
                            "level": section.get("level", 1),
                            "description": section.get("description")
                        }
                        for section in outline_data
                    ],
                    "word_count": word_count,
                    "tone": tone.lower()
                }
                
                result = make_api_request("generate-content", data=payload)
                
                st.session_state.content = result
                st.session_state.current_step = "content_generated"
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error generating content: {str(e)}")
    
    # Display generated content if available
    if st.session_state.content:
        st.subheader("Generated Article")
        
        content_data = st.session_state.content.get("content", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Word Count", content_data.get("word_count", 0))
        with col2:
            st.metric("Status", st.session_state.content.get("status", ""))
        with col3:
            st.metric("Meta Title Length", len(content_data.get("meta_title", "")))
        
        st.markdown("### Meta Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Meta Title:**")
            st.code(content_data.get("meta_title", ""))
        with col2:
            st.write("**Meta Description:**")
            st.code(content_data.get("meta_description", ""))
        
        st.markdown("### Article Content")
        st.markdown(content_data.get("html", ""), unsafe_allow_html=True)
        
        # Download options
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                label="📥 Download as HTML",
                data=content_data.get("html", ""),
                file_name=f"{st.session_state.selected_topic.replace(' ', '_')}.html",
                mime="text/html"
            )
        with col2:
            st.download_button(
                label="📥 Download as Text",
                data=content_data.get("plain_text", ""),
                file_name=f"{st.session_state.selected_topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )


def render_wordpress_section():
    """Render WordPress publishing section."""
    if not st.session_state.content:
        st.warning("Please generate content first")
        return
    
    st.header("Step 5: Publish to WordPress")
    
    content_data = st.session_state.content.get("content", {})
    
    st.info("📢 Publish your generated content directly to WordPress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        post_status = st.selectbox(
            "Post Status",
            ["draft", "publish", "pending"],
            help="Choose whether to save as draft or publish immediately"
        )
    
    with col2:
        post_title = st.text_input(
            "Post Title",
            value=st.session_state.selected_topic,
            help="The title of the WordPress post"
        )
    
    tags = st.text_input(
        "Tags (comma-separated)",
        placeholder="e.g., SEO, Marketing, Content",
        help="Enter tags separated by commas"
    )
    
    if st.button("🚀 Publish to WordPress", use_container_width=True, key="publish_wp_btn"):
        with st.spinner("Publishing to WordPress..."):
            try:
                payload = {
                    "title": post_title,
                    "content": content_data.get("html", ""),
                    "meta_description": content_data.get("meta_description", ""),
                    "status": post_status,
                    "tags": [tag.strip() for tag in tags.split(",") if tag.strip()]
                }
                
                result = make_api_request("publish", data=payload)
                
                st.success(f"""
                ✅ Successfully published!
                
                Post ID: {result.get("post_id")}
                Link: {result.get("link")}
                Status: {result.get("status")}
                """)
                
                st.session_state.current_step = "published"
            
            except Exception as e:
                st.error(f"❌ Error publishing to WordPress: {str(e)}")
                st.info("💡 Tip: Make sure WordPress is configured in the .env file with valid credentials.")


def main():
    """Main Streamlit application."""
    initialize_session_state()
    render_header()
    
    # Sidebar with navigation
    with st.sidebar:
        st.header("Navigation")
        
        steps = ["Input", "Topics", "Outline", "Content", "WordPress"]
        
        # Show available steps
        current_step_map = {
            "input": 0,
            "topics_generated": 1,
            "topic_selected": 2,
            "outline_generated": 3,
            "content_generated": 4,
            "published": 4
        }
        
        current_idx = current_step_map.get(st.session_state.current_step, 0)
        
        for idx, step in enumerate(steps):
            status = "✅" if idx < current_idx else "🔄" if idx == current_idx else "⏭️"
            st.write(f"{status} {step}")
        
        st.divider()
        
        # API Status
        st.subheader("API Status")
        try:
            response = requests.get(f"{API_BASE_URL.replace('/api', '')}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Cannot Connect to Backend")
        
        st.info(f"API URL: {API_BASE_URL}")
    
    # Main content area
    if st.session_state.current_step == "input" or st.session_state.current_step == "input":
        render_input_section()
    
    if st.session_state.current_step in ["topics_generated", "topic_selected", "outline_generated", "content_generated"]:
        if st.session_state.topics:
            render_topics_section()
    
    if st.session_state.current_step in ["topic_selected", "outline_generated", "content_generated"]:
        if st.session_state.selected_topic:
            render_outline_section()
    
    if st.session_state.current_step in ["outline_generated", "content_generated"]:
        if st.session_state.outline:
            render_content_section()
    
    if st.session_state.current_step in ["content_generated", "published"]:
        if st.session_state.content:
            render_wordpress_section()


if __name__ == "__main__":
    main()

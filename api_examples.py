"""
API Examples - SEO Content Tool
Collection of examples showing how to use each endpoint
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# ============================================================================
# EXAMPLE 1: Generate Topics
# ============================================================================

def example_generate_topics():
    """
    Generate 10 SEO-optimized blog topics.
    
    This is the first step in the content creation pipeline.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Generate Topics")
    print("="*60)
    
    payload = {
        "niche": "Digital Marketing",
        "primary_keyword": "SEO Best Practices 2024",
        "target_audience": "Small business owners and marketing professionals",
        "tone": "professional"
    }
    
    print(f"\nRequest to: {API_BASE_URL}/generate-topics")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate-topics",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"\nResponse Status: {response.status_code}")
        print(f"Topics Generated: {len(result['topics'])}")
        
        for i, topic in enumerate(result['topics'], 1):
            print(f"  {i}. {topic}")
        
        return result['topics'][0] if result['topics'] else None
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


# ============================================================================
# EXAMPLE 2: Generate Outline
# ============================================================================

def example_generate_outline(topic: str = None):
    """
    Generate a content outline with H1/H2/H3 structure and FAQ questions.
    
    Requires: A topic from generate_topics
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Generate Outline")
    print("="*60)
    
    if not topic:
        topic = "10 SEO Best Practices That Drive Real Results in 2024"
    
    payload = {
        "topic": topic,
        "primary_keyword": "SEO Best Practices 2024",
        "target_audience": "Small business owners"
    }
    
    print(f"\nRequest to: {API_BASE_URL}/generate-outline")
    print(f"Topic: {topic}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate-outline",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"\nResponse Status: {response.status_code}")
        
        outline = result.get("outline", [])
        print(f"Outline Sections: {len(outline)}")
        print("\nOutline Structure:")
        
        for section in outline[:5]:
            level = section["level"]
            heading = section["heading"]
            indent = "  " * (level - 1)
            print(f"{indent}{'#' * level} {heading}")
        
        if len(outline) > 5:
            print(f"  ... and {len(outline) - 5} more sections")
        
        faq = result.get("faq_questions", [])
        print(f"\nFAQ Questions: {len(faq)}")
        for i, question in enumerate(faq[:3], 1):
            print(f"  {i}. {question}")
        
        if len(faq) > 3:
            print(f"  ... and {len(faq) - 3} more questions")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


# ============================================================================
# EXAMPLE 3: Generate Content
# ============================================================================

def example_generate_content(topic: str = None, outline: dict = None):
    """
    Generate full SEO-optimized article content.
    
    Requires: Topic and outline from previous steps
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Generate Content (Full Article)")
    print("="*60)
    
    if not topic:
        topic = "10 SEO Best Practices That Drive Real Results in 2024"
    
    if not outline:
        outline = [
            {"heading": "Introduction", "level": 1},
            {"heading": "Why SEO Matters", "level": 2},
            {"heading": "Best Practice 1", "level": 2}
        ]
    
    payload = {
        "topic": topic,
        "primary_keyword": "SEO Best Practices 2024",
        "outline": outline,
        "word_count": 1500,  # Shorter for demo
        "target_audience": "Small business owners",
        "tone": "professional"
    }
    
    print(f"\nRequest to: {API_BASE_URL}/generate-content")
    print(f"Topic: {topic}")
    print(f"Word Count: {payload['word_count']}")
    print("This may take 1-2 minutes...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate-content",
            json=payload,
            timeout=180  # 3 minutes timeout
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"\nResponse Status: {response.status_code}")
        
        content = result.get("content", {})
        print(f"\nArticle Generated:")
        print(f"  Word Count: {content.get('word_count')}")
        print(f"  Meta Title: {content.get('meta_title')}")
        print(f"  Meta Description: {content.get('meta_description')}")
        
        print(f"\nFirst 300 characters of content:")
        text = content.get('plain_text', '')[:300]
        print(f"  {text}...")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


# ============================================================================
# EXAMPLE 4: Publish to WordPress
# ============================================================================

def example_publish_to_wordpress(content_data: dict = None):
    """
    Publish generated content to WordPress.
    
    Requires: Generated content from previous step
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Publish to WordPress")
    print("="*60)
    
    if not content_data:
        content_data = {
            "content": {
                "html": "<h1>Test Article</h1><p>This is a test.</p>",
                "meta_description": "Test article meta description"
            }
        }
    
    payload = {
        "title": "10 SEO Best Practices That Drive Real Results in 2024",
        "content": content_data.get("content", {}).get("html", ""),
        "meta_description": content_data.get("content", {}).get("meta_description", ""),
        "status": "draft",  # "draft" or "publish"
        "tags": ["SEO", "Marketing", "Content"]
    }
    
    print(f"\nRequest to: {API_BASE_URL}/publish")
    print(f"Title: {payload['title']}")
    print(f"Status: {payload['status']}")
    print(f"Tags: {payload['tags']}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/publish",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"\nResponse Status: {response.status_code}")
        print(f"Publication Result:")
        print(f"  Post ID: {result.get('post_id')}")
        print(f"  Status: {result.get('status')}")
        print(f"  Link: {result.get('link')}")
        print(f"  Message: {result.get('message')}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        if "Cannot connect" in str(e):
            print("Note: WordPress credentials may not be configured in .env")
        return None


# ============================================================================
# EXAMPLE 5: Check WordPress Connection
# ============================================================================

def example_check_wordpress():
    """
    Check if WordPress is properly configured and accessible.
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Check WordPress Connection")
    print("="*60)
    
    print(f"\nRequest to: {API_BASE_URL}/wordpress/status")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/wordpress/status",
            timeout=10
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"\nResponse Status: {response.status_code}")
        print(f"WordPress Status:")
        print(f"  Status: {result.get('status')}")
        print(f"  URL: {result.get('wordpress_url')}")
        print(f"  Message: {result.get('message')}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None


# ============================================================================
# EXAMPLE 6: Full Workflow
# ============================================================================

def example_full_workflow():
    """
    Complete workflow: Generate topics -> Outline -> Content -> Publish
    """
    print("\n" + "="*70)
    print("COMPLETE WORKFLOW: Topics -> Outline -> Content -> WordPress")
    print("="*70)
    
    # Step 1: Generate topics
    print("\n[1/4] Generating topics...")
    topics = example_generate_topics()
    
    if not topics:
        print("Failed to generate topics. Stopping workflow.")
        return
    
    # Step 2: Generate outline
    print("\n[2/4] Generating outline...")
    outline_result = example_generate_outline(topics)
    
    if not outline_result:
        print("Failed to generate outline. Stopping workflow.")
        return
    
    outline = outline_result.get("outline", [])
    
    # Step 3: Generate content
    print("\n[3/4] Generating content...")
    content_result = example_generate_content(topics, outline)
    
    if not content_result:
        print("Failed to generate content. Stopping workflow.")
        return
    
    # Step 4: Publish to WordPress (optional)
    print("\n[4/4] Publishing to WordPress (optional)...")
    print("Uncomment the line below to actually publish:")
    print("# publish_result = example_publish_to_wordpress(content_result)")
    
    print("\n✓ Workflow completed!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║          SEO Content Tool - API Examples                      ║
    ║                                                                ║
    ║  Make sure the FastAPI backend is running:                    ║
    ║  python -m app.main                                           ║
    ║                                                                ║
    ║  Also ensure your OpenAI API key is configured in .env        ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Run examples
    print("\nRunning API examples...\n")
    
    try:
        # Simple individual examples (faster)
        print("\n" + "="*70)
        print("Running individual endpoint examples...")
        print("="*70)
        
        example_generate_topics()
        example_generate_outline()
        example_generate_content()
        example_check_wordpress()
        
        # Uncomment to publish (requires WordPress setup)
        # example_publish_to_wordpress()
        
        # Full workflow example (takes longer)
        run_full_workflow = input("\nRun full workflow? (y/n): ").lower() == 'y'
        
        if run_full_workflow:
            example_full_workflow()
    
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

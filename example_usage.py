"""
Quick Start Example - Testing the SEO Content Tool
This script demonstrates how to use the API programmatically.
"""

import asyncio
import httpx
import json
from typing import List, Dict


class SEOContentToolClient:
    """Client for interacting with the SEO Content Tool API."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        """Initialize the client."""
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()
    
    async def generate_topics(
        self,
        niche: str,
        keyword: str,
        audience: str = "",
        tone: str = "professional"
    ) -> List[str]:
        """Generate blog topics."""
        payload = {
            "niche": niche,
            "primary_keyword": keyword,
            "target_audience": audience,
            "tone": tone
        }
        
        response = await self.session.post(
            f"{self.base_url}/generate-topics",
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result["topics"]
    
    async def generate_outline(
        self,
        topic: str,
        keyword: str,
        audience: str = ""
    ) -> Dict:
        """Generate content outline."""
        payload = {
            "topic": topic,
            "primary_keyword": keyword,
            "target_audience": audience
        }
        
        response = await self.session.post(
            f"{self.base_url}/generate-outline",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def generate_content(
        self,
        topic: str,
        keyword: str,
        outline: List[Dict],
        word_count: int = 2000,
        audience: str = "",
        tone: str = "professional"
    ) -> Dict:
        """Generate full article content."""
        payload = {
            "topic": topic,
            "primary_keyword": keyword,
            "outline": outline,
            "word_count": word_count,
            "target_audience": audience,
            "tone": tone
        }
        
        response = await self.session.post(
            f"{self.base_url}/generate-content",
            json=payload,
            timeout=180.0  # 3 minutes timeout for content generation
        )
        response.raise_for_status()
        return response.json()
    
    async def publish_to_wordpress(
        self,
        title: str,
        content: str,
        meta_description: str,
        status: str = "draft",
        tags: List[str] = None
    ) -> Dict:
        """Publish to WordPress."""
        payload = {
            "title": title,
            "content": content,
            "meta_description": meta_description,
            "status": status,
            "tags": tags or []
        }
        
        response = await self.session.post(
            f"{self.base_url}/publish",
            json=payload
        )
        response.raise_for_status()
        return response.json()


async def main():
    """Main example demonstrating the full workflow."""
    
    print("=" * 60)
    print("SEO Content Tool - Quick Start Example")
    print("=" * 60)
    
    # Configuration
    NICHE = "Digital Marketing"
    KEYWORD = "SEO Best Practices 2024"
    AUDIENCE = "Small business owners and marketing professionals"
    TONE = "professional"
    
    try:
        async with SEOContentToolClient() as client:
            # Step 1: Generate Topics
            print("\n📝 Step 1: Generating blog topics...")
            print(f"Niche: {NICHE}")
            print(f"Keyword: {KEYWORD}")
            
            topics = await client.generate_topics(
                niche=NICHE,
                keyword=KEYWORD,
                audience=AUDIENCE,
                tone=TONE
            )
            
            print(f"\n✓ Generated {len(topics)} topics:")
            for i, topic in enumerate(topics, 1):
                print(f"  {i}. {topic}")
            
            # Step 2: Select a topic and generate outline
            selected_topic = topics[0]
            print(f"\n📋 Step 2: Generating outline for: {selected_topic}")
            
            outline_response = await client.generate_outline(
                topic=selected_topic,
                keyword=KEYWORD,
                audience=AUDIENCE
            )
            
            outline = outline_response["outline"]
            faq = outline_response["faq_questions"]
            
            print(f"\n✓ Generated outline with {len(outline)} sections")
            print("Outline structure:")
            for section in outline[:5]:  # Show first 5 sections
                level = section["level"]
                heading = section["heading"]
                indent = "  " * (level - 1)
                print(f"  {indent}{'#' * level} {heading}")
            if len(outline) > 5:
                print(f"  ... and {len(outline) - 5} more sections")
            
            print(f"\n✓ Generated {len(faq)} FAQ questions")
            
            # Step 3: Generate full content
            print(f"\n✍️  Step 3: Generating full article content...")
            print("This may take 1-2 minutes...")
            
            content_response = await client.generate_content(
                topic=selected_topic,
                keyword=KEYWORD,
                outline=outline,
                word_count=1500,  # Shorter for demo
                audience=AUDIENCE,
                tone=TONE
            )
            
            content = content_response["content"]
            
            print(f"\n✓ Generated article:")
            print(f"  Word count: {content['word_count']}")
            print(f"  Meta title: {content['meta_title']}")
            print(f"  Meta description: {content['meta_description']}")
            
            # Show first 200 characters
            plain_text_preview = content['plain_text'][:200] + "..."
            print(f"\n  Preview: {plain_text_preview}")
            
            # Step 4: (Optional) Publish to WordPress
            print(f"\n🚀 Step 4: Publishing to WordPress (optional)...")
            print("To publish, uncomment the code below and ensure WordPress is configured")
            
            # Uncomment to actually publish:
            """
            try:
                wp_response = await client.publish_to_wordpress(
                    title=selected_topic,
                    content=content["html"],
                    meta_description=content["meta_description"],
                    status="draft",
                    tags=["SEO", "Marketing", "Content"]
                )
                
                print(f"\n✓ Published to WordPress!")
                print(f"  Post ID: {wp_response['post_id']}")
                print(f"  Status: {wp_response['status']}")
                print(f"  Link: {wp_response['link']}")
            except Exception as e:
                print(f"✗ WordPress publishing failed: {e}")
                print("Make sure WordPress credentials are configured in .env")
            """
            
            # Save content to file
            print(f"\n💾 Saving content to file...")
            
            filename = selected_topic.replace(" ", "_").lower()[:30] + ".html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{content['meta_title']}</title>
    <meta name="description" content="{content['meta_description']}">
</head>
<body>
    {content['html']}
</body>
</html>
""")
            
            print(f"✓ Saved to: {filename}")
            
            print("\n" + "=" * 60)
            print("✅ Example completed successfully!")
            print("=" * 60)
            
    except ConnectionError:
        print("\n❌ Error: Cannot connect to API at http://localhost:8000")
        print("Make sure FastAPI server is running: python -m app.main")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("1. FastAPI server is running")
        print("2. OpenAI API key is configured in .env")
        print("3. Internet connection is working")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

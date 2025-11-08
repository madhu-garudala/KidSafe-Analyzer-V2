"""
Video generation using D-ID API for realistic animated character explanations.
"""

import os
import re
import time
import requests
from typing import Dict, Optional


class VideoGenerator:
    """Generate animated character videos using D-ID API."""
    
    def __init__(self):
        """Initialize video generator."""
        self.did_api_key = os.environ.get('DID_API_KEY', '').strip()
        
        # Auto-fix: Add "Basic " prefix if not present
        if self.did_api_key and not self.did_api_key.startswith('Basic '):
            self.did_api_key = f'Basic {self.did_api_key}'
            print("   ℹ️  Auto-added 'Basic ' prefix to D-ID API key")
        
        # Character image - D-ID requires HUMAN faces (cartoon dogs don't work)
        # Using a friendly, child-friendly human presenter
        # Options:
        # 1. Emma - friendly woman with warm voice
        # 2. Upload your own human character image
        self.character_image_url = "https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.jpeg"
        
    def create_short_script(self, analysis: str, product_name: str) -> str:
        """
        Create a SHORT script (verdict + 1 sentence).
        
        Args:
            analysis: Full analysis text
            product_name: Name of the product
            
        Returns:
            Short script for video
        """
        # Extract verdict
        verdict_match = re.search(r'VERDICT:\s*\[?(GOOD|MODERATE|BAD)[^\]]*\]?', analysis, re.IGNORECASE)
        verdict = verdict_match.group(1).upper() if verdict_match else 'MODERATE'
        
        # Extract the most important concern or benefit (first line of detailed analysis)
        # Look for red flags or key points
        red_flag_match = re.search(r'\*\*Red Flag Ingredients:\*\*\s*([^\n]+)', analysis)
        sugar_match = re.search(r'sugar.*?(\d+)g', analysis.lower())
        
        # Create SHORT scripts based on verdict
        if verdict == 'GOOD':
            script = f"{product_name} is a GOOD choice! It has healthy, natural ingredients that are great for kids."
        elif verdict == 'BAD':
            if red_flag_match:
                reason = red_flag_match.group(1).strip()[:100]  # First 100 chars
                script = f"{product_name} is BAD for kids. It contains artificial ingredients and chemicals you should avoid."
            else:
                script = f"{product_name} is BAD for kids. It has too much added sugar and unhealthy ingredients."
        else:  # MODERATE
            script = f"{product_name} is MODERATE. It's okay as an occasional treat, but choose healthier options most of the time."
        
        return script
    
    def generate_video(self, script: str) -> Optional[str]:
        """
        Generate video using D-ID API.
        
        Args:
            script: Short script text
            
        Returns:
            Video URL or None if failed
        """
        if not self.did_api_key:
            print("⚠️  D-ID API key not configured")
            print("   Set DID_API_KEY in .env file to enable video generation")
            return None
        
        print("🎬 Creating animated video with D-ID...")
        print(f"   Script: {script}")
        
        url = "https://api.d-id.com/talks"
        
        # FIXED: D-ID uses the API key directly in Authorization header
        headers = {
            "Authorization": f"{self.did_api_key}",
            "Content-Type": "application/json"
        }
        
        # Use D-ID's built-in text-to-speech with a reliable voice
        payload = {
            "source_url": self.character_image_url,
            "script": {
                "type": "text",
                "input": script,
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                }
            },
            "config": {
                "fluent": True,
                "pad_audio": 0
            }
        }
        
        try:
            # Create video
            print("   📤 Sending request to D-ID...")
            response = requests.post(url, json=payload, headers=headers)
            
            # Debug response
            print(f"   Response status: {response.status_code}")
            
            if response.status_code == 401:
                print("   ❌ D-ID API key is invalid or not authorized")
                print("   Please check your DID_API_KEY in .env file")
                print("   Get your key from: https://studio.d-id.com/account")
                return None
            
            response.raise_for_status()
            
            talk_data = response.json()
            talk_id = talk_data.get('id')
            
            if not talk_id:
                print(f"   ❌ D-ID API error: {talk_data}")
                return None
            
            print(f"   ✅ Video ID: {talk_id}")
            print("   ⏳ Processing video (15-30 seconds)...")
            
            # Poll for video status
            status_url = f"{url}/{talk_id}"
            max_polls = 60  # 60 seconds max
            
            for i in range(max_polls):
                time.sleep(1)
                
                status_response = requests.get(status_url, headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get('status')
                
                if status == 'done':
                    video_url = status_data.get('result_url')
                    print(f"   ✅ Video ready! {video_url}")
                    return video_url
                    
                elif status == 'error' or status == 'rejected':
                    error_msg = status_data.get('error', {}).get('description', 'Unknown error')
                    print(f"   ❌ Video generation failed: {error_msg}")
                    return None
                
                # Show progress
                if (i + 1) % 10 == 0:
                    print(f"   ⏳ Still processing... ({i + 1}s)")
            
            print("   ⚠️  Video generation timed out")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response status: {e.response.status_code}")
                print(f"   Response body: {e.response.text}")
            import traceback
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"   ❌ Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_explanation_video(
        self,
        analysis: str,
        product_name: str
    ) -> Dict[str, any]:
        """
        Create full explanation video from analysis.
        
        Args:
            analysis: Full analysis text
            product_name: Name of the product
            
        Returns:
            Dict with video_url, script, and status
        """
        try:
            # Create SHORT script
            script = self.create_short_script(analysis, product_name)
            print(f"\n📝 Script: {script}")
            
            # Generate video
            video_url = self.generate_video(script)
            
            return {
                'success': video_url is not None,
                'video_url': video_url,
                'script': script,
                'type': 'video',
                'has_api': bool(self.did_api_key)
            }
            
        except Exception as e:
            print(f"❌ Error creating video: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                'success': False,
                'video_url': None,
                'script': script if 'script' in locals() else '',
                'error': str(e),
                'type': 'video',
                'has_api': bool(self.did_api_key)
            }

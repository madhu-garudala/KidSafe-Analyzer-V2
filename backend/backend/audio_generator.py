"""
Simple audio generation using Google Text-to-Speech (FREE alternative to D-ID).
"""

import os
import re
import base64
from typing import Optional, Dict
from gtts import gTTS
import io


class AudioGenerator:
    """Generate audio explanations using free Google TTS."""
    
    def __init__(self):
        """Initialize audio generator."""
        pass
    
    def extract_key_points(self, analysis: str, product_name: str) -> str:
        """
        Extract key points from analysis for script.
        
        Args:
            analysis: Full analysis text
            product_name: Name of the product
            
        Returns:
            Child-friendly script
        """
        # Extract verdict
        verdict_match = re.search(r'VERDICT:\s*\[?(GOOD|MODERATE|BAD)[^\]]*\]?', analysis, re.IGNORECASE)
        verdict = verdict_match.group(1).upper() if verdict_match else 'MODERATE'
        
        # Extract quick summary
        summary_match = re.search(r'\*\*Quick Summary:\*\*\s*([^\n]+)', analysis)
        summary = summary_match.group(1).strip() if summary_match else ''
        
        # Build script based on verdict
        if verdict == 'GOOD':
            emoji = '✅'
            intro = f"Great news! {product_name} got a GOOD rating!"
            closing = "This is a great choice! Enjoy!"
        elif verdict == 'BAD':
            emoji = '❌'
            intro = f"Heads up! {product_name} got a BAD rating."
            closing = "Maybe save this for very special treats, and ask for healthier snacks instead!"
        else:  # MODERATE
            emoji = '⚠️'
            intro = f"{product_name} got a MODERATE rating."
            closing = "It's okay sometimes, but try to choose healthier options most of the time!"
        
        # Build child-friendly script (keep it short)
        script = f"""Hi! I'm Berry, your friendly food helper!

{intro}

{summary if summary else 'Let me tell you what you should know.'}

{closing}"""
        
        return script.strip()
    
    def generate_audio(self, text: str) -> Optional[str]:
        """
        Generate audio using Google Text-to-Speech (gTTS - FREE!).
        
        Args:
            text: Script text to convert to speech
            
        Returns:
            Base64 encoded audio data or None if failed
        """
        try:
            print("🎙️  Generating audio with Google TTS (free)...")
            
            # Create TTS object
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Convert to base64 for easy transmission
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            
            print(f"   ✅ Audio generated ({len(audio_base64)} bytes)")
            return audio_base64
            
        except Exception as e:
            print(f"   ❌ Error generating audio: {str(e)}")
            return None
    
    def create_explanation_audio(
        self, 
        analysis: str, 
        product_name: str
    ) -> Dict[str, any]:
        """
        Create audio explanation from analysis.
        
        Args:
            analysis: Full analysis text
            product_name: Name of the product
            
        Returns:
            Dict with audio_data, script, and status
        """
        try:
            # Extract script
            script = self.extract_key_points(analysis, product_name)
            print(f"\n📝 Script generated ({len(script)} chars)")
            
            # Generate audio
            audio_base64 = self.generate_audio(script)
            
            return {
                'success': audio_base64 is not None,
                'audio_base64': audio_base64,
                'script': script,
                'type': 'audio'  # Changed from 'video'
            }
            
        except Exception as e:
            print(f"❌ Error creating audio: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                'success': False,
                'audio_base64': None,
                'script': script if 'script' in locals() else '',
                'error': str(e),
                'type': 'audio'
            }


#!/bin/bash

echo "🧪 Testing D-ID Video Generation..."
echo ""

response=$(curl -s -X POST http://localhost:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "cereal_name": "Oreos",
    "ingredients": "Sugar, High Fructose Corn Syrup, Artificial Colors (Red 40)",
    "generate_video": true
  }')

# Extract video section
echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    video = data.get('video', {})
    print('📊 Video Generation Result:')
    print(f'   Success: {video.get(\"success\", False)}')
    print(f'   Has API: {video.get(\"has_api\", False)}')
    print(f'   Script: {video.get(\"script\", \"N/A\")}')
    if video.get('video_url'):
        print(f'   ✅ Video URL: {video.get(\"video_url\")}')
    else:
        print(f'   ❌ No video URL')
        if 'error' in video:
            print(f'   Error: {video.get(\"error\")}')
except Exception as e:
    print(f'Error parsing response: {e}')
    print('Raw response:')
    for line in sys.stdin:
        print(line)
"


# 🐶 Animated Character Setup Guide

## Overview

Your app now features **Berry the Blue Dog** - an animated character that explains why products are good or bad for kids! This uses cutting-edge AI to create realistic talking videos.

---

## 🎬 How It Works

1. **Analysis Complete** → Extract key points
2. **ElevenLabs** → Generate child-friendly voice narration
3. **D-ID** → Animate character with lip-sync
4. **Display** → Show video to user!

**Result**: A personalized animated video for every product! 🎉

---

## 🔑 API Setup (Required)

### Step 1: ElevenLabs API (Voice Generation)

1. **Sign up**: https://elevenlabs.io/
2. **Choose Plan**:
   - **Free**: 10,000 characters/month (~30-40 videos)
   - **Starter**: $5/month, 30,000 characters (~100+ videos)
3. **Get API Key**:
   - Go to Profile → API Keys
   - Click "Generate API Key"
   - Copy the key

### Step 2: D-ID API (Video Animation)

1. **Sign up**: https://www.d-id.com/
2. **Choose Plan**:
   - **Trial**: 20 free video credits
   - **Lite**: $5.9/month, 100 videos
   - **Pro**: $29/month, 500 videos
3. **Get API Key**:
   - Go to Settings → API
   - Copy your API Key (starts with "Basic ...")

### Step 3: Character Image (Optional)

**Default**: We use a generic blue dog emoji (🐶)

**Custom Character**: 
- Upload your own character image (PNG, 512x512px recommended)
- Host it online (Imgur, Cloudinary, etc.)
- Add URL to `.env` file

---

## ⚙️ Configuration

Add these to `backend/.env`:

```bash
# Existing keys
OPENAI_API_KEY=sk-your-key-here
LANGCHAIN_API_KEY=your-key-here

# NEW: Video Generation APIs
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
DID_API_KEY=your-d-id-api-key-here

# Optional: Custom character image
CHARACTER_IMAGE_URL=https://your-image-url.png

# Optional: Different voice (see ElevenLabs voices)
ELEVENLABS_VOICE_ID=ErXwobaYiN019PkySvjV
```

---

## 🚀 Testing

1. **Add API keys** to `backend/.env`
2. **Restart backend**:
   ```bash
   # Stop current backend (Ctrl+C)
   cd backend
   source venv/bin/activate
   python main.py
   ```
3. **Test with a product**:
   - Search for "Oreos"
   - Wait ~30-60 seconds for video generation
   - Watch Berry explain why Oreos got their rating!

---

## 💰 Cost Breakdown

### Per Video:
- **ElevenLabs**: ~300 characters = ~$0.005 (less than 1 cent)
- **D-ID**: 1 video = ~$0.06 (6 cents)
- **Total**: ~$0.065 per video (~6.5 cents)

### Monthly (100 videos):
- **ElevenLabs**: $5/month (Starter plan)
- **D-ID**: $5.9/month (Lite plan, 100 videos)
- **Total**: ~$11/month for 100 personalized videos

**Very affordable** for the amazing user experience! 🎉

---

## 🎨 Character Customization

### Option 1: Use Our Blue Dog (Default)
- Simple dog emoji: 🐶
- No extra setup needed
- Works immediately

### Option 2: Custom Character Image
1. **Create/Find Image**:
   - Square image (512x512px recommended)
   - Clear face (for lip-sync)
   - PNG or JPG format
   - Blue dog inspired by Bluey (avoid exact copy for copyright)

2. **Host Image**:
   ```bash
   # Option A: Imgur
   - Upload to imgur.com
   - Get direct link: https://i.imgur.com/xxxxx.png
   
   # Option B: Cloudinary (free 25GB)
   - Sign up at cloudinary.com
   - Upload image
   - Get URL
   ```

3. **Add to .env**:
   ```bash
   CHARACTER_IMAGE_URL=https://i.imgur.com/your-image.png
   ```

### Option 3: Commission Character (Recommended for Production)
- **Cost**: $50-200 on Fiverr
- Get unique character design
- Legally safe (you own it)
- More professional
- Can trademark your character

---

## 🎙️ Voice Options

ElevenLabs has many child-friendly voices:

| Voice ID | Name | Description |
|----------|------|-------------|
| `ErXwobaYiN019PkySvjV` | Antoni | Friendly, clear (default) |
| `EXAVITQu4vr4xnSDxMaL` | Bella | Young, cheerful |
| `pNInz6obpgDQGcFmaJgB` | Adam | Warm, friendly |

To change voice, update `.env`:
```bash
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
```

---

## 🐛 Troubleshooting

### "Video generation requires API setup"
**Problem**: API keys not configured
**Solution**: Add `ELEVENLABS_API_KEY` and `DID_API_KEY` to `.env`

### "Video generation failed"
**Problem**: Invalid API keys or quota exceeded
**Solution**: 
- Check keys are correct
- Verify API quotas: ElevenLabs dashboard, D-ID dashboard
- Check backend terminal for error messages

### "Video takes too long" (>2 minutes)
**Problem**: D-ID processing queue
**Solution**: 
- Normal during peak times
- Video will eventually complete
- Script shown immediately as fallback

### "Character doesn't look right"
**Problem**: Wrong image URL or image format
**Solution**:
- Use square images (512x512px)
- PNG or JPG format
- Must be publicly accessible URL

---

## 📊 Analytics

Check your usage:

**ElevenLabs**: https://elevenlabs.io/app/usage
**D-ID**: https://studio.d-id.com/account

Set up alerts to avoid overages!

---

## 🎯 User Experience Flow

### With APIs Configured:
```
1. User searches "Oreos"
   ↓
2. Analysis completes (10 seconds)
   ↓
3. "Generating animated explanation..." (loading)
   ↓
4. Script shown immediately (while video generates)
   ↓
5. Video ready! (30-60 seconds total)
   ↓
6. Auto-plays Berry explaining the rating
```

### Without APIs:
```
1. User searches "Oreos"
   ↓
2. Analysis completes (10 seconds)
   ↓
3. Shows script only with message:
   "Video generation requires API setup"
   ↓
4. Still works, just no video
```

---

## 🌟 Pro Tips

1. **Start with Trial**: Use free trials to test before committing
2. **Monitor Usage**: Set up alerts for API quotas
3. **Cache Popular Products**: Pre-generate videos for top 20 products
4. **Fallback Gracefully**: App works fine without videos (shows script)
5. **Custom Character**: Invest in unique character for brand identity

---

## 📝 Example Video Script

For "Oreos" (BAD rating):

```
Hi there! I'm Berry, your friendly food helper! 
Let me tell you about Oreos. ❌

Heads up! Oreos got a BAD rating.

This product contains high fructose corn syrup 
and artificial flavors which aren't great for growing bodies.

Here's what you should know:

1. High fructose corn syrup: This type of sugar is 
   linked to health issues in kids
2. Artificial flavors: Unnecessary chemicals we don't need
3. Lots of added sugar: More than your daily limit!

Maybe save these for very special treats, and 
ask for healthier snacks instead!
```

**Duration**: ~30 seconds
**Child-friendly**: ✅
**Informative**: ✅
**Engaging**: ✅

---

## 🚀 Next Steps

1. **Sign up** for ElevenLabs and D-ID
2. **Add API keys** to `backend/.env`
3. **Restart backend** server
4. **Test** with a product
5. **Enjoy** personalized videos! 🎉

---

## 💡 Future Enhancements

Possible improvements:
- Multiple characters (choose favorites)
- Different languages
- Longer videos with more details
- Interactive quizzes
- Share videos on social media
- Character merchandise 🧸

---

**Ready to make your app amazing?** Set up the APIs and watch Berry come to life! 🐶✨

---

## 📞 Support

- **ElevenLabs**: support@elevenlabs.io
- **D-ID**: support@d-id.com
- **Documentation**: Check README.md and DEVELOPMENT.md

---

**Your app just got 100x more engaging!** 🎉


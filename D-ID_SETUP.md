# 🎬 D-ID Setup Guide for Animated Videos

## What You'll Get

Real animated videos of a cartoon character (like Bluey) explaining why products are GOOD/BAD/MODERATE in **one simple sentence**.

Example: 
> "Oreos is BAD for kids. It contains artificial ingredients and chemicals you should avoid."

---

## 🆓 Get D-ID API Key (Free Trial)

### Step 1: Sign Up
1. Go to: **https://studio.d-id.com**
2. Click "Start Free" or "Sign Up"
3. Create account (email + password or Google)
4. ✅ You get **20 free credits** ($20 value!)

### Step 2: Get API Key
1. After login, click your profile (top right)
2. Go to **"Account Settings"** or **"API"**
3. Click **"Create API Key"** or copy existing key
4. Copy the key (looks like: `Basic bXl1c2VybmFtZTpteXBhc3N3b3Jk` or just `abcd1234...`)

### Step 3: Add to .env File
```bash
cd ~/Desktop/AI_MakerSpace/Code/KidSafe-Analyzer-V2/backend

# Edit .env file
nano .env
```

Add this line:
```bash
DID_API_KEY=your_actual_key_here
```

**Note:** 
- If your key starts with "Basic ", include it: `DID_API_KEY=Basic abcd1234...`
- If it's just letters/numbers, add as-is: `DID_API_KEY=abcd1234...`

### Step 4: Restart Backend
```bash
# Stop backend (CTRL+C in backend terminal)

# Restart
cd ~/Desktop/AI_MakerSpace/Code/KidSafe-Analyzer-V2/backend
source venv/bin/activate
python main.py
```

### Step 5: Test It!
1. Refresh frontend
2. Search for "Oreos" or any product
3. Wait 15-30 seconds
4. 🎬 Watch the animated video!

---

## 💰 Pricing

| Plan | Credits | Cost | Videos |
|------|---------|------|--------|
| **Free Trial** | 20 | $0 | ~20 videos |
| Lite | 100 | $29/mo | ~100 videos |
| Basic | 300 | $49/mo | ~300 videos |
| Pro | Unlimited | Custom | Unlimited |

**Each video = ~1 credit** (15-30 seconds)

---

## 🎯 What Changed?

### Before (Audio Player)
- ❌ No real video
- ❌ Just audio + text animation
- ❌ Not very engaging

### After (D-ID Video)
- ✅ Real animated character video
- ✅ Character lip-syncs with voice
- ✅ Short, simple messages (GOOD/BAD + reason)
- ✅ Like watching a cartoon!

---

## 📝 Video Scripts

Scripts are now **super short** (1-2 sentences):

### GOOD Products
> "Seven Sundays Cereal is a GOOD choice! It has healthy, natural ingredients that are great for kids."

### BAD Products  
> "Oreos is BAD for kids. It contains artificial ingredients and chemicals you should avoid."

### MODERATE Products
> "Cheerios is MODERATE. It's okay as an occasional treat, but choose healthier options most of the time."

---

## 🎨 Character Image

Currently using a placeholder cartoon dog image. You can customize:

1. **Find or create** a Bluey-style character image
2. **Upload** to image hosting (imgur, imgbb, etc.)
3. **Edit** `backend/backend/video_generator.py`:
   ```python
   self.character_image_url = "https://your-image-url.com/character.png"
   ```
4. **Restart** backend

**Image Requirements:**
- Format: PNG, JPG, or WebP
- Size: 512x512px recommended
- Face: Clear, front-facing
- Background: Solid color or transparent

---

## 🔧 Troubleshooting

### "401 Unauthorized" Error
- ❌ API key is wrong or missing
- ✅ Check `.env` file has correct key
- ✅ Restart backend after adding key

### Video Takes Too Long
- D-ID typically takes 15-30 seconds
- If longer, check D-ID dashboard for status

### "Out of Credits" Error
- Free trial gives 20 credits
- Need to upgrade plan on D-ID website

### Video Not Playing
- Check video URL in browser
- Check browser console for errors
- Try different browser

---

## 📊 Monitoring Usage

Check your D-ID credits:
1. Go to: https://studio.d-id.com
2. Click profile → "Account Settings"
3. See "Credits Remaining"

Each product analysis = 1 credit used.

---

## 🎉 Alternative: No D-ID Key?

If you don't want to set up D-ID, the app still shows:
- ✅ The short message (text)
- ✅ Setup instructions
- ✅ Full analysis below

It just won't generate the animated video.

---

## 💡 Tips

1. **Test with 1 product first** before analyzing many
2. **Free trial = 20 videos** - use wisely!
3. **Videos are cached** by D-ID for 24 hours
4. **Shorter scripts** = faster generation + less cost

---

## 🚀 Ready to Test!

1. Add `DID_API_KEY` to `.env`
2. Restart backend
3. Search for "Oreos"
4. Wait 15-30 seconds
5. 🎬 Enjoy the animated video!

Questions? Check backend terminal for detailed logs.


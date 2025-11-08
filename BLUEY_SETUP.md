# 🐶 How to Add Bluey Character to Videos

## 🎯 Quick Setup

You have 3 options to get Bluey working:

---

## ✅ **Option 1: Use Pre-Hosted Bluey Image** (Easiest)

I'll try a few public Bluey URLs. Update your code with one that works:

### Test These URLs:

**Try each one in order:**

```python
# Bluey from Bluey Wiki
"https://static.wikia.nocookie.net/bluey/images/e/e5/Bluey_Heeler.png"

# Bluey PNG from Fandom
"https://blueypedia.fandom.com/wiki/Special:FilePath/Bluey_Heeler.png"

# Alternative Bluey image
"https://i.imgur.com/7XqVZHY.png"
```

---

## ✅ **Option 2: Upload Your Own Bluey Image** (Recommended)

### Step 1: Get a Good Bluey Image
- Search Google Images: "Bluey character PNG front facing"
- Look for images where Bluey is:
  - ✅ Facing forward (not side view)
  - ✅ Clear face visible
  - ✅ High resolution (at least 512x512)
  - ✅ PNG or JPG format

### Step 2: Upload to Free Image Hosting

**Use ImgBB (no account needed):**

1. Go to: **https://imgbb.com**
2. Click "Start uploading"
3. Select your Bluey image
4. Wait for upload
5. **Copy the "Direct link"** (ends in .png or .jpg)
6. Use that URL in your code!

**Alternative: Use Imgur:**

1. Go to: **https://imgur.com/upload**
2. Upload Bluey image
3. Right-click uploaded image → "Copy image address"
4. Use that URL!

---

## ✅ **Option 3: Use a Different Cartoon Character** (Quick Test)

If you just want to test, try these working cartoon-style characters:

```python
# Cartoon woman (friendly, child-friendly)
"https://create-images-results.d-id.com/DefaultPresenters/Emma_f/image.jpeg"

# Cartoon man (friendly voice)
"https://create-images-results.d-id.com/DefaultPresenters/Oliver_m/image.jpeg"
```

---

## 🔧 **How to Update the Code:**

### **Edit the file:**
```bash
nano ~/Desktop/AI_MakerSpace/Code/KidSafe-Analyzer-V2/backend/backend/video_generator.py
```

### **Find line 26** and replace the URL:

**Before:**
```python
self.character_image_url = "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg"
```

**After (use your Bluey URL):**
```python
self.character_image_url = "YOUR_BLUEY_IMAGE_URL_HERE"
```

### **Save and restart backend:**
```bash
# Press CTRL+X, then Y, then Enter to save in nano
# Or use the command below to update directly
```

---

## 🚀 **Quick Update Command:**

**I can help you update it! Just tell me which image you want to use and I'll update the code for you.**

---

## 📋 **Image Requirements for D-ID:**

✅ **MUST HAVE:**
- Front-facing character
- Clear face/eyes visible
- Good lighting
- At least 512x512 pixels

❌ **AVOID:**
- Side profiles
- Blurry images
- Very small images
- Complex backgrounds (transparent is best)

---

## 💡 **Recommended Approach:**

1. **Search Google Images:** "Bluey character transparent PNG"
2. **Download a good image** (front-facing, clear face)
3. **Upload to imgbb.com**
4. **Copy the direct link**
5. **Tell me the URL** and I'll update the code for you!

---

## 🎬 **Testing:**

After updating, restart backend and test with "Oreos" - you should see Bluey speaking!

Need help? Just share the Bluey image URL you want to use!


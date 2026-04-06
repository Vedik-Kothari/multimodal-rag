from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import subprocess
import os

# 1. Text to Speech
print("Generating audio...")
text = "Welcome to the Quarter 3 Earnings Call. Looking at our first slide, you'll see our revenue reached 10 million dollars, up 45 percent. On the next slide, we highlight our new product launch happening in November."
tts = gTTS(text=text, lang='en')
tts.save("audio.mp3")

# 2. Graphics (Slides)
print("Generating slides...")
def create_slide(text, filename, bg_color="navy"):
    img = Image.new('RGB', (1280, 720), color=bg_color)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    d.text((100, 300), text, fill=(255, 255, 255), font=font)
    img.save(filename)

create_slide("Q3 Earnings Call\nWelcome Guests", "slide1.jpg", "#1e3a8a")
create_slide("Revenue Growth\n$10M (Up 45%)", "slide2.jpg", "#064e3b")
create_slide("Product Roadmap\nNovember Launch", "slide3.jpg", "#7f1d1d")

# 3. Create video segments
print("Stitching video...")
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

with open("slides.txt", "w") as f:
    f.write("file 'slide1.jpg'\nduration 7\n")
    f.write("file 'slide2.jpg'\nduration 7\n")
    f.write("file 'slide3.jpg'\nduration 7\n")
    f.write("file 'slide3.jpg'\n")

# 4. ffmpeg command
cmd = [
    ffmpeg, "-y",
    "-f", "concat",
    "-i", "slides.txt",
    "-i", "audio.mp3",
    "-pix_fmt", "yuv420p",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-shortest",
    "q3_earnings_presentation.mp4"
]
subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Cleanup
for f in ["audio.mp3", "slide1.jpg", "slide2.jpg", "slide3.jpg", "slides.txt"]:
    if os.path.exists(f): os.remove(f)

print("Generated successfully: q3_earnings_presentation.mp4")

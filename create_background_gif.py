from PIL import Image, ImageDraw
import random

# Create a 800x600 black image
width, height = 800, 600
image = Image.new("RGB", (width, height), "black")
draw = ImageDraw.Draw(image)

# Draw 100 random white stars (1-2px)
for _ in range(100):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    size = random.randint(1, 2)
    draw.ellipse([x, y, x + size, y + size], fill="white")

# Save as GIF with low color depth
image.save("background.gif", "GIF", optimize=True)
print("Created background.gif")
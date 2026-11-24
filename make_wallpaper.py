"""Generate a minimal dark wallpaper to match a black / graphite iPhone.

Usage: python3 make_wallpaper.py
Writes wallpaper-graphite.png (1290x2796, the iPhone Pro Max screen size;
it also fits smaller iPhones, which crop it slightly).
"""
import numpy as np
from PIL import Image

W, H = 1290, 2796
rng = np.random.default_rng(7)

y, x = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = x / W, y / H

# Base: near-black with a faint cool tint, slightly lighter at the top.
top = np.array([14, 14, 17], np.float32)
bottom = np.array([5, 5, 6], np.float32)
img = top * (1 - v[..., None]) + bottom * v[..., None]

# Graphite sheen: a soft diagonal band of light, like light on titanium.
d = (u * 0.55 + v * 0.85) - 0.62
sheen = np.exp(-(d / 0.11) ** 2) * 0.9 + np.exp(-((d + 0.06) / 0.025) ** 2) * 0.35
img += sheen[..., None] * np.array([30, 31, 35], np.float32)

# Faint steel-blue glow, low and off to one side, kept behind the dock area.
g = np.exp(-(((u - 0.78) / 0.42) ** 2 + ((v - 0.86) / 0.22) ** 2))
img += g[..., None] * np.array([10, 16, 26], np.float32)

# Vignette to keep the edges deep black (good for OLED).
r = np.sqrt(((u - 0.5) / 0.75) ** 2 + ((v - 0.45) / 0.85) ** 2)
img *= np.clip(1.15 - 0.55 * r**2, 0.35, 1.0)[..., None]

# Fine grain prevents colour banding in the dark gradients.
img += rng.normal(0, 0.9, (H, W, 1)).astype(np.float32)

Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").save(
    "wallpaper-graphite.png", optimize=True
)
print("saved wallpaper-graphite.png", W, "x", H)

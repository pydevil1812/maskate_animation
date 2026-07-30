from PIL import Image, ImageOps
from rembg import remove
import math
SIZE = 64

def pixelate(img, size = SIZE):
    w, h = img.size
    if w>= h:
        new_w, new_h = size, round(size*h / w)
    else:
        new_w, new_h = round(size*w / h), size
    small_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return small_img
def preview(img, scale = 8):
    w, h = img.size
    new_img = img.resize((w*scale, h*scale), Image.Resampling.NEAREST)
    return new_img
def find_subject(img):
    img = remove(img)
    frame = img.getbbox()
    img = img.crop(frame)
    return img

def quantize(img, colors = 16):
    alpha = img.getchannel('A')
    alpha = alpha.point(lambda v: 255 if v >= 128 else 0)
    img = img.convert('RGB')
    img = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    img = img.convert('RGB')
    img.putalpha(alpha)
    return img

def make_frames(img, count= 4, amp = 0.06, size = SIZE):
    frames = []
    w, h = img.size
    for i in range(count):
        phase = 2*math.pi * i /count
        sx = 1+amp*math.sin(phase)
        sy = 1-amp*math.sin(phase)
        scaled = img.resize((round(w*sx), round(h*sy)), Image.Resampling.NEAREST)
        cell = round(size*(1+amp))
        canvas = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
        x = (cell-scaled.width)//2
        y = cell - scaled.height
        canvas.paste(scaled, (x, y), scaled)
        frames.append(canvas)
    return frames

def build_spritesheet(frames):
    w, h = frames[0].size
    canvas = Image.new('RGBA', (w*len(frames), h))
    for i, frame in enumerate(frames):
        canvas.paste(frame, (i*w, 0))
    return canvas

orig_img = ImageOps.exif_transpose(Image.open("input/funtik.jpg"))
sprite = quantize(pixelate(find_subject(orig_img)))
frames = make_frames(sprite)
sheet = build_spritesheet(frames)

sheet.save('output/spritesheet.png')

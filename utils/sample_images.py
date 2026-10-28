"""
Sample Image Generator for Multimodal Construction Intelligence Platform.
Generates realistic procedural synthetic construction test scenes and concrete defect specimens
using Pillow, enabling instant 1-click evaluation without external downloads.
"""

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import math
import random

def get_image_bytes(img: Image.Image) -> bytes:
    """Convert PIL image to PNG byte stream."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def generate_safety_sample_violation() -> Image.Image:
    """
    Synthesize an active construction elevation showing scaffolding and worker hazards:
    - Worker A at 6m elevation missing safety harness & hard hat
    - Worker B on ground with high-vis vest
    - Unsecured scaffolding planks & exposed edge
    """
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(210, 225, 240)) # overcast sky
    draw = ImageDraw.Draw(img)

    # Ground soil/concrete slab
    draw.rectangle([0, 480, width, height], fill=(95, 85, 75))
    draw.line([0, 480, width, 480], fill=(60, 50, 40), width=4)

    # RCC Frame Building Under Construction
    # Columns
    for col_x in [100, 320, 540, 740]:
        draw.rectangle([col_x, 80, col_x + 50, 480], fill=(160, 165, 170), outline=(120, 125, 130), width=2)
    # Beams / Slabs
    for slab_y in [180, 320, 460]:
        draw.rectangle([80, slab_y, 760, slab_y + 35], fill=(145, 150, 155), outline=(100, 105, 110), width=2)

    # Scaffolding Tubes (Steel tubular staging)
    scaff_color = (180, 190, 205)
    for x in range(350, 700, 90):
        draw.line([x, 150, x, 480], fill=scaff_color, width=4)
    for y in range(180, 480, 70):
        draw.line([340, y, 710, y], fill=scaff_color, width=4)
        # Cross braces
        draw.line([350, y, 440, y + 70], fill=(160, 170, 185), width=2)
        draw.line([440, y, 350, y + 70], fill=(160, 170, 185), width=2)
        draw.line([440, y, 530, y + 70], fill=(160, 170, 185), width=2)

    # Scaffold working platform plank (unsecured wooden board)
    draw.rectangle([345, 245, 620, 255], fill=(185, 140, 90), outline=(130, 90, 50), width=2)

    # Worker 1 (at height 250px - VIOLATION: No helmet, no harness, reaching over ledge)
    # Torso
    draw.rectangle([480, 200, 505, 245], fill=(40, 80, 160)) # Blue shirt (no hi-vis)
    # Head (Dark hair, NO HARD HAT)
    draw.ellipse([484, 180, 502, 200], fill=(210, 160, 130))
    draw.arc([484, 178, 502, 192], start=180, end=360, fill=(30, 20, 15), width=4)
    # Arms reaching out
    draw.line([480, 210, 460, 195], fill=(210, 160, 130), width=5)
    draw.line([505, 210, 525, 205], fill=(210, 160, 130), width=5)
    # Legs (Regular jeans, no visible harness leg straps)
    draw.line([488, 245, 488, 275], fill=(50, 60, 80), width=6)
    draw.line([498, 245, 502, 275], fill=(50, 60, 80), width=6)

    # Worker 2 on ground (COMPLIANT: Yellow hardhat, neon vest)
    # Head & Yellow Hard Hat
    draw.ellipse([180, 400, 196, 416], fill=(220, 170, 140))
    draw.chord([176, 394, 200, 410], start=180, end=360, fill=(255, 215, 0), outline=(200, 160, 0), width=2)
    draw.line([174, 403, 202, 403], fill=(240, 190, 0), width=2)
    # Torso with Neon Hi-Vis Vest
    draw.rectangle([176, 416, 200, 450], fill=(57, 255, 20)) # High-vis lime green
    draw.line([184, 416, 184, 450], fill=(240, 240, 240), width=3) # Reflective strip
    draw.line([192, 416, 192, 450], fill=(240, 240, 240), width=3)
    # Boots
    draw.rectangle([178, 465, 188, 478], fill=(40, 30, 25))
    draw.rectangle([188, 465, 198, 478], fill=(40, 30, 25))

    # Warning Annotations for Visual Realism
    draw.rectangle([20, 20, 360, 65], fill=(15, 23, 42, 220), outline=(245, 158, 11), width=2)
    draw.text((32, 28), "SITE MONITORING CAM - ZONE 4B", fill=(245, 158, 11))
    draw.text((32, 44), "ELEVATED SCAFFOLDING & FACADE WORKS", fill=(220, 220, 220))

    return img

def generate_safety_sample_compliant() -> Image.Image:
    """Synthesize a fully OSHA/IS 456 compliant crew on ground excavation."""
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(190, 210, 230))
    draw = ImageDraw.Draw(img)

    # Excavation trench & safety barrier
    draw.rectangle([0, 400, width, height], fill=(120, 95, 70))
    draw.rectangle([0, 430, 450, height], fill=(70, 50, 35)) # Deep cut
    # Trench trench box / shoring plates
    draw.rectangle([40, 430, 420, 580], fill=(180, 140, 30), outline=(130, 100, 20), width=3)
    # Safety barricade tape
    for x in range(0, width, 40):
        draw.line([x, 395, x + 25, 405], fill=(255, 60, 60), width=4)
        draw.line([x + 25, 395, x + 50, 405], fill=(255, 255, 255), width=4)

    # 2 Workers: Both fully geared (helmets, vests, steel-toe boots)
    for offset_x in [520, 640]:
        # Hard Hat
        draw.chord([offset_x - 14, 320, offset_x + 14, 342], start=180, end=360, fill=(255, 220, 0), outline=(200, 170, 0), width=2)
        draw.ellipse([offset_x - 10, 330, offset_x + 10, 348], fill=(215, 170, 140))
        # Hi-Vis Orange Vest with silver bands
        draw.rectangle([offset_x - 15, 348, offset_x + 15, 385], fill=(255, 105, 0))
        draw.line([offset_x - 8, 348, offset_x - 8, 385], fill=(240, 240, 240), width=3)
        draw.line([offset_x + 8, 348, offset_x + 8, 385], fill=(240, 240, 240), width=3)
        # Steel toe boots
        draw.rectangle([offset_x - 14, 395, offset_x - 4, 405], fill=(30, 30, 30))
        draw.rectangle([offset_x + 4, 395, offset_x + 14, 405], fill=(30, 30, 30))

    draw.rectangle([20, 20, 380, 65], fill=(15, 23, 42, 220), outline=(16, 185, 129), width=2)
    draw.text((32, 28), "SITE MONITORING CAM - ZONE 1A", fill=(16, 185, 129))
    draw.text((32, 44), "DEEP TRENCH EXCAVATION & SHORING CREW", fill=(220, 220, 220))
    return img

def generate_crack_structural_shear() -> Image.Image:
    """
    Synthesize an RCC Beam with a classic 45-degree diagonal shear crack near the support.
    Diagnostic characteristics: High structural severity, shear failure, IS 456 Cl. 40.
    """
    width, height = 750, 500
    img = Image.new("RGB", (width, height), color=(175, 178, 180))
    draw = ImageDraw.Draw(img)

    # Concrete texture noise
    random.seed(42)
    for _ in range(12000):
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)
        shade = random.randint(145, 195)
        img.putpixel((rx, ry), (shade, shade, shade))

    # RCC Column Support on Left
    draw.rectangle([0, 0, 160, height], fill=(140, 143, 146), outline=(110, 112, 115), width=3)
    # Beam soffit line
    draw.line([160, 80, width, 80], fill=(110, 112, 115), width=3)
    draw.line([160, 420, width, 420], fill=(110, 112, 115), width=3)

    # 45-Degree Diagonal Structural Shear Crack starting near column face
    # Jittery zigzag path
    crack_points = []
    cur_x, cur_y = 190, 400
    crack_points.append((cur_x, cur_y))
    while cur_x < 460 and cur_y > 110:
        cur_x += random.randint(12, 22)
        cur_y -= random.randint(14, 25)
        # add micro-jitter
        jitter_x = cur_x + random.randint(-4, 4)
        jitter_y = cur_y + random.randint(-3, 3)
        crack_points.append((jitter_x, jitter_y))

    # Draw dark crack core (width ~3-4mm equivalent)
    for i in range(len(crack_points) - 1):
        p1 = crack_points[i]
        p2 = crack_points[i + 1]
        draw.line([p1, p2], fill=(25, 20, 18), width=5)
        # Draw micro-spalling edge
        draw.line([(p1[0]+1, p1[1]), (p2[0]+1, p2[1])], fill=(85, 75, 70), width=2)
        # Branch crack
        if i == 5:
            draw.line([p1, (p1[0] + 35, p1[1] + 25)], fill=(40, 35, 30), width=2)

    # Forensic scale ruler
    draw.rectangle([520, 360, 710, 450], fill=(245, 245, 230), outline=(20, 20, 20), width=2)
    draw.text((540, 370), "STRUCTURAL FORENSIC SCALE", fill=(20, 20, 20))
    for tick_x in range(530, 700, 15):
        draw.line([tick_x, 410, tick_x, 435], fill=(0, 0, 0), width=2)
    draw.text((530, 436), "0 mm", fill=(0, 0, 0))
    draw.text((660, 436), "100 mm", fill=(0, 0, 0))

    # Water staining & efflorescence halo around crack
    for p in crack_points[::3]:
        draw.ellipse([p[0]-15, p[1]-15, p[0]+15, p[1]+15], fill=(200, 195, 185, 60))

    return img

def generate_crack_spalling_rebar() -> Image.Image:
    """
    Synthesize concrete spalling with exposed, corroding carbon steel rebar.
    Diagnostic characteristics: Carbonation, cover loss, active oxidation delamination.
    """
    width, height = 750, 500
    img = Image.new("RGB", (width, height), color=(168, 170, 172))
    draw = ImageDraw.Draw(img)

    # Concrete grain noise
    random.seed(101)
    for _ in range(10000):
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)
        s = random.randint(140, 190)
        img.putpixel((rx, ry), (s, s, s))

    # Spalled cavity (rough irregular pocket where concrete cover fractured)
    spall_poly = [
        (220, 180), (310, 150), (440, 160), (540, 200), (570, 280),
        (530, 360), (410, 390), (280, 370), (210, 300), (195, 230)
    ]
    draw.polygon(spall_poly, fill=(110, 105, 100), outline=(70, 65, 60))

    # Rust bleeding halos
    for _ in range(30):
        bx = random.randint(230, 530)
        by = random.randint(200, 350)
        draw.ellipse([bx, by, bx + random.randint(20, 60), by + random.randint(10, 40)], fill=(160, 80, 30))

    # Exposed vertical Rebar (corroded ribbed bar)
    for rebar_x in [320, 450]:
        # Dark corroded steel core
        draw.rectangle([rebar_x, 120, rebar_x + 24, 420], fill=(130, 55, 25), outline=(70, 25, 10), width=2)
        # Rib deformations
        for rib_y in range(130, 410, 14):
            draw.line([rebar_x, rib_y, rebar_x + 24, rib_y + 4], fill=(180, 85, 35), width=3)
            draw.line([rebar_x, rib_y + 6, rebar_x + 24, rib_y + 10], fill=(60, 20, 10), width=2)

    # Diagnostic HUD stamp
    draw.rectangle([30, 30, 340, 75], fill=(15, 23, 42), outline=(239, 68, 68), width=2)
    draw.text((42, 38), "NDT STRUCTURAL INTEGRITY SCAN", fill=(239, 68, 68))
    draw.text((42, 54), "TARGET: SPALLING & REBAR CORROSION", fill=(240, 240, 240))

    return img

def generate_crack_hairline_plaster() -> Image.Image:
    """
    Synthesize superficial hairline shrinkage/crazing cracks on rendered plaster.
    Diagnostic characteristics: Non-structural, cosmetic plaster shrinkage, width <0.15mm.
    """
    width, height = 750, 500
    img = Image.new("RGB", (width, height), color=(225, 222, 215)) # Off-white paint
    draw = ImageDraw.Draw(img)

    random.seed(99)
    # Spiderweb hairline network
    centers = [(300, 240), (450, 280), (360, 340)]
    for cx, cy in centers:
        for angle_deg in range(0, 360, 45):
            angle = math.radians(angle_deg + random.randint(-15, 15))
            cur_x, cur_y = cx, cy
            for step in range(random.randint(6, 12)):
                next_x = cur_x + math.cos(angle) * random.randint(15, 30) + random.randint(-3, 3)
                next_y = cur_y + math.sin(angle) * random.randint(15, 30) + random.randint(-3, 3)
                draw.line([(cur_x, cur_y), (next_x, next_y)], fill=(120, 115, 110), width=1)
                cur_x, next_y = next_x, next_y

    draw.rectangle([30, 30, 320, 70], fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.text((42, 38), "SURFACE INTEGRITY ASSESSMENT", fill=(16, 185, 129))
    draw.text((42, 52), "TARGET: PLASTER DRYING SHRINKAGE", fill=(240, 240, 240))
    return img

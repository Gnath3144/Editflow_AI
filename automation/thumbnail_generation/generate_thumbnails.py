"""
Codealytica Automated YouTube Thumbnail Generation Pipeline - Enhanced Edition
Generates high-CTR, 1280x720 professional technology YouTube thumbnails for Day 01 Generative AI lessons.
"""

import json
import logging
import math
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ThumbnailGenerator")

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "thumbnail_config.json"
ASSETS_DIR = SCRIPT_DIR / "assets"
OUTPUT_DIR = SCRIPT_DIR / "output"
PREVIEWS_DIR = SCRIPT_DIR / "previews"
REPORT_PATH = SCRIPT_DIR / "THUMBNAIL_GENERATION_REPORT.md"

THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720
ASPECT_RATIO = 16 / 9
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB


def get_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    """Loads fonts from Windows fonts or fallbacks."""
    for fn in [name, name.lower(), name.upper()]:
        p = Path(f"C:/Windows/Fonts/{fn}")
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    for fb in ["segoeuib.ttf", "impact.ttf", "arialbd.ttf", "arial.ttf"]:
        p = Path(f"C:/Windows/Fonts/{fb}")
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def hex_to_rgba(hex_str: str, alpha: int = 255) -> Tuple[int, int, int, int]:
    r, g, b = hex_to_rgb(hex_str)
    return (r, g, b, alpha)


class EnhancedThumbnailComposer:
    def __init__(self, config_data: dict):
        self.config = config_data
        self.brand = config_data.get("brand", {})
        self.colors = self.brand.get("colors", {})

    def create_cinematic_background(self, theme_hex: str) -> Image.Image:
        """Renders deep obsidian/navy gradient with cybernetic grid and radial glow."""
        base = Image.new("RGBA", (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (7, 11, 20, 255))
        draw = ImageDraw.Draw(base)

        # Gradient
        c1 = (5, 8, 16)
        c2 = (11, 22, 44)
        for y in range(THUMBNAIL_HEIGHT):
            t = y / THUMBNAIL_HEIGHT
            r = int(c1[0] * (1 - t) + c2[0] * t)
            g = int(c1[1] * (1 - t) + c2[1] * t)
            b = int(c1[2] * (1 - t) + c2[2] * t)
            draw.line([(0, y), (THUMBNAIL_WIDTH, y)], fill=(r, g, b, 255))

        # Neon aura behind right side hero element
        glow = Image.new("RGBA", (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        theme_rgb = hex_to_rgb(theme_hex)

        cx, cy = 940, 360
        max_r = 450
        for r in range(max_r, 0, -20):
            alpha = int((1.0 - (r / max_r)) * 48)
            glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(theme_rgb[0], theme_rgb[1], theme_rgb[2], alpha))

        glow = glow.filter(ImageFilter.GaussianBlur(35))
        base = Image.alpha_composite(base, glow)

        # Tech Grid lines
        grid = Image.new("RGBA", (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (0, 0, 0, 0))
        grid_draw = ImageDraw.Draw(grid)
        for x in range(0, THUMBNAIL_WIDTH, 48):
            grid_draw.line([(x, 0), (x, THUMBNAIL_HEIGHT)], fill=(255, 255, 255, 6), width=1)
        for y in range(0, THUMBNAIL_HEIGHT, 48):
            grid_draw.line([(0, y), (THUMBNAIL_WIDTH, y)], fill=(255, 255, 255, 6), width=1)

        return Image.alpha_composite(base, grid)

    def draw_brand_header(self, draw: ImageDraw.Draw, item: dict) -> None:
        """Top brand identity banner."""
        x = 55
        y = 42

        # Cyan Brand Pill
        font_brand = get_font("segoeuib.ttf", 24)
        font_series = get_font("segoeuib.ttf", 15)

        # Glowing cyan bullet
        draw.ellipse([x, y + 4, x + 16, y + 18], fill=hex_to_rgb(self.colors.get("cyan", "#00E5FF")))

        # CODEALYTICA brand text
        draw.text((x + 24, y - 2), "CODEALYTICA", fill=(255, 255, 255), font=font_brand)

        # Vertical separator
        sep_x = x + 210
        draw.line([(sep_x, y + 2), (sep_x, y + 24)], fill=(60, 80, 115), width=2)

        # Series metadata
        lesson_text = f"GENERATIVE AI • DAY 01 • LESSON {item['lesson_num']:02d}"
        draw.text((sep_x + 18, y + 4), lesson_text, fill=hex_to_rgb(self.colors.get("cyan", "#00E5FF")), font=font_series)

        # Right-side topic badge
        tag = item.get("tag_badge", "AI TUTORIAL")
        font_tag = get_font("segoeuib.ttf", 15)
        bbox = draw.textbbox((0, 0), tag, font=font_tag)
        tw = bbox[2] - bbox[0]

        px2 = THUMBNAIL_WIDTH - 55
        px1 = px2 - tw - 32
        py1 = y - 4
        py2 = py1 + 34

        theme_rgb = hex_to_rgb(item.get("theme_color", "#00E5FF"))
        draw.rounded_rectangle([px1, py1, px2, py2], radius=17, fill=(12, 22, 38, 230), outline=theme_rgb, width=2)
        draw.text((px1 + 16, py1 + 7), tag, fill=theme_rgb, font=font_tag)

    def draw_typography_left(self, draw: ImageDraw.Draw, item: dict) -> None:
        """Draws headline, metric pill, and supporting subtitle on the left zone."""
        headline = item["headline"]
        supporting = item["supporting_text"]
        metric_badge = item.get("metric_badge", "")
        theme_rgb = hex_to_rgb(item.get("theme_color", "#00E5FF"))
        highlight_rgb = hex_to_rgb(item.get("highlight_color", "#FFD600"))

        start_x = 55
        start_y = 120

        # 1. Metric Hook Pill (Top of headline)
        if metric_badge:
            font_hook = get_font("segoeuib.ttf", 16)
            bbox = draw.textbbox((0, 0), metric_badge, font=font_hook)
            hw = bbox[2] - bbox[0]
            draw.rounded_rectangle(
                [start_x, start_y, start_x + hw + 34, start_y + 36],
                radius=18,
                fill=theme_rgb
            )
            draw.text((start_x + 17, start_y + 7), metric_badge, fill=(5, 8, 15), font=font_hook)
            start_y += 56

        # 2. Huge Punchy Headline
        font_hl = get_font("impact.ttf", 84)
        if "headline_lines" in item:
            lines = item["headline_lines"]
        else:
            words = headline.split()
            lines = []
            cur = []
            for w in words:
                test = " ".join(cur + [w])
                bbox = draw.textbbox((0, 0), test, font=font_hl)
                if bbox[2] - bbox[0] > 550 and cur:
                    lines.append(" ".join(cur))
                    cur = [w]
                else:
                    cur.append(w)
            if cur:
                lines.append(" ".join(cur))

        line_h = 92
        for line in lines:
            # Drop shadow
            draw.text((start_x + 4, start_y + 4), line, fill=(0, 0, 0, 240), font=font_hl)
            draw.text((start_x + 2, start_y + 2), line, fill=(0, 0, 0, 255), font=font_hl)

            # Color logic: numbers or question/exclamation marks get highlighted
            color = highlight_rgb if any(c.isdigit() or c in "?!" for c in line) else (255, 255, 255)
            draw.text((start_x, start_y), line, fill=color, font=font_hl)
            start_y += line_h

        start_y += 18

        # 3. High-Contrast Subtitle Pill
        if supporting:
            font_sub = get_font("segoeuib.ttf", 26)
            bbox = draw.textbbox((0, 0), supporting, font=font_sub)
            sw = bbox[2] - bbox[0]
            sh = bbox[3] - bbox[1]

            bx1 = start_x
            by1 = start_y
            bx2 = bx1 + sw + 44
            by2 = by1 + sh + 24

            draw.rounded_rectangle([bx1, by1, bx2, by2], radius=12, fill=(10, 20, 38, 250), outline=theme_rgb, width=3)
            draw.text((bx1 + 22, by1 + 10), supporting, fill=(255, 255, 255), font=font_sub)

    def draw_footer_trust(self, draw: ImageDraw.Draw, item: dict) -> None:
        """Bottom safe-area trust points."""
        y = THUMBNAIL_HEIGHT - 60
        x = 55
        font_ft = get_font("segoeuib.ttf", 15)

        points = {
            1: "✓ 100% Free & Open Source   •   ✓ Complete Data Privacy",
            2: "✓ Google DeepMind Weights   •   ✓ Architecture Deep Dive",
            3: "✓ Ultra-Low RAM Footprint   •   ✓ Tested on 8GB Hardware",
            4: "✓ Real Windows Task Manager •   ✓ Live GPU Telemetry",
            5: "✓ Parameter Sizing Guide    •   ✓ Quality vs Speed Matrix",
            6: "✓ Generative AI Foundations •   ✓ 3 Core Engineering Rules",
        }
        text = points.get(item["lesson_num"], "✓ Codealytica Engineering")
        draw.text((x, y), text, fill=(130, 155, 185), font=font_ft)

    # -------------------------------------------------------------
    # CUSTOM HERO VISUAL GENERATORS FOR EACH LESSON
    # -------------------------------------------------------------

    def build_hero_card_frame(self, w: int, h: int, title: str, theme_hex: str) -> Tuple[Image.Image, ImageDraw.Draw, int, int]:
        """Creates a stylish terminal window container."""
        card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)

        # Body background
        draw.rounded_rectangle([0, 0, w, h], radius=16, fill=(13, 20, 36, 250))

        # Title bar
        draw.rounded_rectangle([0, 0, w, 38], radius=16, fill=(22, 33, 54, 255))
        draw.rectangle([0, 20, w, 38], fill=(22, 33, 54, 255))

        # Window dots
        draw.ellipse([14, 13, 24, 23], fill=(255, 95, 87))
        draw.ellipse([30, 13, 40, 23], fill=(254, 188, 46))
        draw.ellipse([46, 13, 56, 23], fill=(40, 201, 64))

        # Title
        font_t = get_font("consolab.ttf", 14)
        draw.text((68, 10), title, fill=(170, 185, 210), font=font_t)

        # Border
        theme_rgb = hex_to_rgb(theme_hex)
        draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, outline=theme_rgb, width=2)

        return card, draw, w, h

    def render_hero_lesson_01(self, raw_frame_path: str, theme_hex: str) -> Image.Image:
        """Lesson 01: Real PowerShell install script + Ollama badge."""
        w, h = 580, 440
        card, draw, cw, ch = self.build_hero_card_frame(w, h, "Administrator: Windows PowerShell — Ollama Install", theme_hex)

        # Real cropped terminal from raw frame (focused on dark terminal window)
        p = Path(raw_frame_path)
        if p.exists():
            raw = Image.open(p).convert("RGBA")
            # Crop pure PowerShell console window: x=195..1290, y=180..560
            crop = raw.crop((195, 180, 1290, 560)).resize((540, 240), Image.Resampling.LANCZOS)
            card.paste(crop, (20, 50))

        # Overlay Callout Badge below terminal
        draw.rounded_rectangle([20, 305, 560, 415], radius=12, fill=(18, 30, 52, 255), outline=hex_to_rgb(theme_hex), width=2)

        font_callout = get_font("segoeuib.ttf", 20)
        font_sub = get_font("segoeuib.ttf", 14)

        # Glowing indicator
        draw.ellipse([38, 325, 52, 339], fill=(0, 230, 118))
        draw.text((62, 320), "LOCAL AI RUNNING OFFLINE", fill=(255, 255, 255), font=font_callout)
        draw.text((62, 355), "• 100% Zero Cloud Latency  • No API Keys Required", fill=(0, 229, 255), font=font_sub)
        draw.text((62, 380), "• Full Data Privacy on Windows 11", fill=(160, 175, 200), font=font_sub)

        return card

    def render_hero_lesson_02(self, raw_frame_path: str, theme_hex: str) -> Image.Image:
        """Lesson 02: Gemma 2B Architecture + Neural Weights."""
        w, h = 580, 440
        card, draw, cw, ch = self.build_hero_card_frame(w, h, "Gemma 2B — DeepMind Model Weights (3.5 GB)", theme_hex)

        # Real cropped terminal
        p = Path(raw_frame_path)
        if p.exists():
            raw = Image.open(p).convert("RGBA")
            crop = raw.crop((100, 160, 1280, 560)).resize((540, 180), Image.Resampling.LANCZOS)
            card.paste(crop, (20, 50))

        # Lower architecture infographic panel
        draw.rounded_rectangle([20, 245, 560, 415], radius=12, fill=(18, 28, 48, 255), outline=(138, 43, 226), width=2)

        # Big 2B typography callout
        font_big = get_font("impact.ttf", 60)
        draw.text((40, 260), "2B", fill=(255, 214, 0), font=font_big)

        font_arch = get_font("segoeuib.ttf", 18)
        font_det = get_font("segoeuib.ttf", 13)

        draw.text((125, 265), "2,000,000,000 PARAMETERS", fill=(255, 255, 255), font=font_arch)
        draw.text((125, 295), "Google DeepMind Gemma Architecture", fill=(0, 229, 255), font=font_det)
        draw.text((125, 320), "• Multi-Head Attention  • Rotary Position Embeddings (RoPE)", fill=(160, 175, 200), font=font_det)
        draw.text((125, 345), "• 18 Layer Transformer  • 2048 Hidden Dimension", fill=(160, 175, 200), font=font_det)
        draw.text((40, 380), "⚡ FITS ENTIRELY INSIDE SYSTEM MEMORY (3.5 GB)", fill=(0, 230, 118), font=font_det)

        return card

    def render_hero_lesson_03(self, raw_frame_path: str, theme_hex: str) -> Image.Image:
        """Lesson 03: Qwen 2.5 0.5B on 8GB RAM Laptop."""
        w, h = 580, 440
        card, draw, cw, ch = self.build_hero_card_frame(w, h, "Qwen 2.5 (0.5B) — Low-Spec Hardware Benchmark", theme_hex)

        p = Path(raw_frame_path)
        if p.exists():
            raw = Image.open(p).convert("RGBA")
            crop = raw.crop((100, 160, 1280, 540)).resize((540, 175), Image.Resampling.LANCZOS)
            card.paste(crop, (20, 50))

        # 8GB RAM Hardware Card
        draw.rounded_rectangle([20, 240, 560, 415], radius=12, fill=(14, 28, 40, 255), outline=(0, 230, 118), width=2)

        # Huge 8GB RAM badge
        font_ram = get_font("impact.ttf", 62)
        draw.text((38, 255), "8GB", fill=(0, 230, 118), font=font_ram)

        font_ram_title = get_font("segoeuib.ttf", 20)
        font_ram_sub = get_font("segoeuib.ttf", 14)

        draw.text((155, 260), "STANDARD LAPTOP COMPATIBLE", fill=(255, 255, 255), font=font_ram_title)
        draw.text((155, 292), "Model Download: Only 394 MB!", fill=(255, 214, 0), font=font_ram_sub)
        draw.text((155, 318), "• In-Memory Working Set: ~650 MB RAM", fill=(170, 190, 215), font=font_ram_sub)
        draw.text((155, 344), "• No Expensive Dedicated GPU Needed", fill=(170, 190, 215), font=font_ram_sub)
        draw.text((38, 380), "🚀 ZERO BARRIER TO LOCAL GENERATIVE AI", fill=(0, 229, 255), font=font_ram_sub)

        return card

    def render_hero_lesson_04(self, raw_frame_path: str, theme_hex: str) -> Image.Image:
        """Lesson 04: Windows Task Manager GPU & CPU Telemetry."""
        w, h = 580, 440
        card, draw, cw, ch = self.build_hero_card_frame(w, h, "Task Manager — Live GPU Telemetry & VRAM", theme_hex)

        p = Path(raw_frame_path)
        if p.exists():
            raw = Image.open(p).convert("RGBA")
            # Crop performance graph in Task Manager: around x=500..1600, y=140..750
            crop = raw.crop((500, 160, 1600, 750)).resize((540, 230), Image.Resampling.LANCZOS)
            card.paste(crop, (20, 50))

        # GPU Telemetry Callout Box
        draw.rounded_rectangle([20, 295, 560, 415], radius=12, fill=(35, 18, 14, 255), outline=(255, 107, 0), width=2)

        # Huge GPU Callout
        font_gpu = get_font("impact.ttf", 54)
        draw.text((36, 310), "47%", fill=(255, 107, 0), font=font_gpu)

        font_gt = get_font("segoeuib.ttf", 19)
        font_gs = get_font("segoeuib.ttf", 13)

        draw.text((140, 312), "LIVE HARDWARE UTILIZATION", fill=(255, 255, 255), font=font_gt)
        draw.text((140, 342), "• Intel UHD + NVIDIA GeForce GTX Active", fill=(255, 214, 0), font=font_gs)
        draw.text((140, 365), "• Real-Time Memory & Tensor Allocation", fill=(170, 185, 205), font=font_gs)
        draw.text((36, 388), "⚡ SEE EXACTLY WHAT HAPPENS INSIDE YOUR PC", fill=(0, 229, 255), font=font_gs)

        return card

    def render_hero_lesson_05(self, raw_frame_path: str, theme_hex: str) -> Image.Image:
        """Lesson 05: Small vs Large AI Comparison (The Star Analogy)."""
        w, h = 580, 440
        card, draw, cw, ch = self.build_hero_card_frame(w, h, "Model Sizing Benchmark — Small vs Large", theme_hex)

        # Split comparison container
        # Left Box: Compact Models
        draw.rounded_rectangle([20, 50, 275, 340], radius=12, fill=(12, 28, 48, 255), outline=(0, 229, 255), width=2)
        font_hdr = get_font("segoeuib.ttf", 18)
        font_bld = get_font("impact.ttf", 36)
        font_dtl = get_font("segoeuib.ttf", 13)

        draw.text((35, 62), "COMPACT AI", fill=(0, 229, 255), font=font_hdr)
        draw.text((35, 90), "0.5B — 2B", fill=(255, 255, 255), font=font_bld)
        draw.text((35, 140), "✦ Like a Red Dwarf Star", fill=(255, 214, 0), font=font_dtl)
        draw.text((35, 168), "• Ultra-fast execution", fill=(170, 190, 215), font=font_dtl)
        draw.text((35, 192), "• Runs on any laptop", fill=(170, 190, 215), font=font_dtl)
        draw.text((35, 216), "• Low power footprint", fill=(170, 190, 215), font=font_dtl)
        draw.text((35, 240), "• Focused task efficiency", fill=(170, 190, 215), font=font_dtl)
        draw.rounded_rectangle([35, 280, 260, 318], radius=8, fill=(0, 229, 255))
        draw.text((65, 288), "DAILY WORKHORSE", fill=(5, 10, 20), font=font_dtl)

        # VS Badge in middle
        draw.ellipse([265, 170, 315, 220], fill=(255, 214, 0), outline=(255, 255, 255), width=3)
        font_vs = get_font("impact.ttf", 26)
        draw.text((276, 178), "VS", fill=(0, 0, 0), font=font_vs)

        # Right Box: Massive Models
        draw.rounded_rectangle([305, 50, 560, 340], radius=12, fill=(35, 15, 25, 255), outline=(255, 61, 113), width=2)
        draw.text((320, 62), "MASSIVE AI", fill=(255, 61, 113), font=font_hdr)
        draw.text((320, 90), "70B — 405B", fill=(255, 255, 255), font=font_bld)
        draw.text((320, 140), "★ Like a Supergiant Star", fill=(255, 214, 0), font=font_dtl)
        draw.text((320, 168), "• Massive reasoning capacity", fill=(170, 190, 215), font=font_dtl)
        draw.text((320, 192), "• Multi-hop logic", fill=(170, 190, 215), font=font_dtl)
        draw.text((320, 216), "• High VRAM requirement", fill=(170, 190, 215), font=font_dtl)
        draw.text((320, 240), "• Server GPU architecture", fill=(170, 190, 215), font=font_dtl)
        draw.rounded_rectangle([320, 280, 545, 318], radius=8, fill=(255, 61, 113))
        draw.text((365, 288), "HEAVYWEIGHT AI", fill=(255, 255, 255), font=font_dtl)

        # Lower takeaway bar
        draw.rounded_rectangle([20, 355, 560, 415], radius=10, fill=(18, 25, 42), outline=(255, 214, 0), width=2)
        draw.text((45, 372), "THE STAR ANALOGY: Bigger isn't always better for your task!", fill=(255, 255, 255), font=font_dtl)

        return card

    def render_hero_lesson_06(self, raw_frame_path: str, theme_hex: str) -> Image.Image:
        """Lesson 06: Generative AI 3 Golden Rules & Course Finale."""
        w, h = 580, 440
        card, draw, cw, ch = self.build_hero_card_frame(w, h, "Generative AI Masterclass — 3 Golden Rules", theme_hex)

        # Day 01 Finale Ribbon
        draw.rounded_rectangle([20, 48, 560, 94], radius=10, fill=(255, 214, 0))
        font_fin = get_font("impact.ttf", 28)
        draw.text((130, 54), "🏆 DAY 01 MASTERCLASS FINALE", fill=(5, 10, 20), font=font_fin)

        font_rule_num = get_font("impact.ttf", 36)
        font_rule_title = get_font("segoeuib.ttf", 17)
        font_rule_sub = get_font("segoeuib.ttf", 13)

        rules = [
            ("1", "NEVER EXPOSE SENSITIVE DATA", "Run private weights locally for sensitive workflows.", (0, 229, 255)),
            ("2", "SIZE YOUR MODEL ACCORDINGLY", "Don't use a 70B rocket to swat a 0.5B fly.", (255, 214, 0)),
            ("3", "VALIDATE CODE & OUTPUTS ALWAYS", "LLMs generate probabilities, not absolute truths.", (0, 230, 118)),
        ]

        start_y = 108
        for num, title, desc, col in rules:
            draw.rounded_rectangle([20, start_y, 560, start_y + 88], radius=10, fill=(15, 26, 44, 255), outline=col, width=2)
            # Number badge
            draw.rounded_rectangle([32, start_y + 16, 76, start_y + 70], radius=8, fill=col)
            draw.text((44, start_y + 20), num, fill=(5, 10, 20), font=font_rule_num)

            # Rule text
            draw.text((92, start_y + 16), title, fill=(255, 255, 255), font=font_rule_title)
            draw.text((92, start_y + 44), desc, fill=(160, 180, 205), font=font_rule_sub)

            start_y += 98

        return card

    def compose_thumbnail(self, item: dict) -> Image.Image:
        """Assembles the complete 1280x720 thumbnail."""
        theme_hex = item.get("theme_color", "#00E5FF")
        lesson_num = item["lesson_num"]
        source_frame = item.get("source_frame", "")

        # 1. Base gradient
        base_img = self.create_cinematic_background(theme_hex)

        # 2. Render Lesson-Specific Hero Visual
        if lesson_num == 1:
            hero_card = self.render_hero_lesson_01(source_frame, theme_hex)
        elif lesson_num == 2:
            hero_card = self.render_hero_lesson_02(source_frame, theme_hex)
        elif lesson_num == 3:
            hero_card = self.render_hero_lesson_03(source_frame, theme_hex)
        elif lesson_num == 4:
            hero_card = self.render_hero_lesson_04(source_frame, theme_hex)
        elif lesson_num == 5:
            hero_card = self.render_hero_lesson_05(source_frame, theme_hex)
        elif lesson_num == 6:
            hero_card = self.render_hero_lesson_06(source_frame, theme_hex)
        else:
            hero_card = self.render_hero_lesson_01(source_frame, theme_hex)

        # Drop shadow behind hero card
        card_w, card_h = hero_card.size
        shadow = Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.rounded_rectangle([15, 15, card_w + 15, card_h + 15], radius=16, fill=(0, 0, 0, 180))
        shadow = shadow.filter(ImageFilter.GaussianBlur(14))

        # Paste hero card on right side: x ~ 650, y ~ 125
        card_x = 645
        card_y = 125
        base_img.paste(shadow, (card_x - 15, card_y - 15), shadow)
        base_img.paste(hero_card, (card_x, card_y), hero_card)

        # 3. Draw Typography & Overlays
        draw = ImageDraw.Draw(base_img)
        self.draw_brand_header(draw, item)
        self.draw_typography_left(draw, item)
        self.draw_footer_trust(draw, item)

        # Convert to RGB
        final_img = Image.new("RGB", base_img.size, (7, 11, 20))
        final_img.paste(base_img, mask=base_img.split()[3])
        return final_img


def validate_thumbnail(img: Image.Image, file_path: Path) -> dict:
    w, h = img.size
    aspect = round(w / h, 4)
    expected_aspect = round(ASPECT_RATIO, 4)

    file_size = file_path.stat().st_size if file_path.exists() else 0
    size_mb = round(file_size / (1024 * 1024), 3)

    is_valid_res = (w == THUMBNAIL_WIDTH and h == THUMBNAIL_HEIGHT)
    is_valid_aspect = (aspect == expected_aspect)
    is_valid_size = (file_size > 0 and file_size <= MAX_FILE_SIZE_BYTES)

    return {
        "width": w,
        "height": h,
        "aspect_ratio": f"{w}:{h} ({aspect})",
        "file_size_bytes": file_size,
        "file_size_mb": size_mb,
        "valid_resolution": is_valid_res,
        "valid_aspect": is_valid_aspect,
        "valid_size": is_valid_size,
        "overall_valid": is_valid_res and is_valid_aspect and is_valid_size,
    }


def create_contact_sheet(thumbnails: List[Tuple[dict, Image.Image]]) -> Path:
    cols = 3
    rows = 2
    thumb_w, thumb_h = 600, 338
    margin = 40
    header_h = 100
    footer_h = 60

    sheet_w = (cols * thumb_w) + ((cols + 1) * margin)
    sheet_h = header_h + (rows * thumb_h) + ((rows + 1) * margin) + footer_h

    sheet = Image.new("RGB", (sheet_w, sheet_h), (8, 14, 24))
    draw = ImageDraw.Draw(sheet)

    font_title = get_font("segoeuib.ttf", 32)
    font_sub = get_font("segoeuib.ttf", 16)
    font_label = get_font("segoeuib.ttf", 14)

    draw.text((margin, 30), "CODEALYTICA — GENERATIVE AI DAY 01 THUMBNAIL SUITE", fill=(0, 229, 255), font=font_title)
    draw.text((margin, 70), "Master Contact Sheet  •  Resolution: 1280x720 (16:9)  •  High-CTR Technology Design System", fill=(160, 175, 200), font=font_sub)

    for idx, (item, img) in enumerate(thumbnails):
        r = idx // cols
        c = idx % cols

        x = margin + c * (thumb_w + margin)
        y = header_h + margin + r * (thumb_h + margin)

        resized = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y))

        theme_rgb = hex_to_rgb(item.get("theme_color", "#00E5FF"))
        draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=theme_rgb, width=2)

        label = f"Lesson {item['lesson_num']:02d}: {item['headline']}  [{item['video_id']}]"
        draw.text((x + 6, y + thumb_h + 8), label, fill=(220, 230, 245), font=font_label)

    contact_path = PREVIEWS_DIR / "contact_sheet_all_six.png"
    sheet.save(contact_path, "PNG", optimize=True)
    logger.info(f"Generated Contact Sheet: {contact_path}")
    return contact_path


def create_mobile_preview(thumbnails: List[Tuple[dict, Image.Image]]) -> Path:
    mobile_w = 400
    mobile_thumb_w = 360
    mobile_thumb_h = int(mobile_thumb_w * 9 / 16)
    item_h = mobile_thumb_h + 90
    total_h = 100 + (len(thumbnails) * item_h) + 40

    preview = Image.new("RGB", (mobile_w, total_h), (15, 15, 15))
    draw = ImageDraw.Draw(preview)

    font_hdr = get_font("segoeuib.ttf", 20)
    font_title = get_font("segoeuib.ttf", 13)
    font_meta = get_font("segoeuib.ttf", 11)

    draw.text((20, 30), "YouTube Mobile Feed Simulation", fill=(255, 255, 255), font=font_hdr)
    draw.text((20, 60), "Testing legibility at 360px mobile card width", fill=(150, 150, 150), font=font_meta)

    curr_y = 100
    for item, img in thumbnails:
        m_thumb = img.resize((mobile_thumb_w, mobile_thumb_h), Image.Resampling.LANCZOS)
        x = (mobile_w - mobile_thumb_w) // 2
        preview.paste(m_thumb, (x, curr_y))

        title_text = item["title"][:58] + "..." if len(item["title"]) > 58 else item["title"]
        draw.text((x, curr_y + mobile_thumb_h + 10), title_text, fill=(255, 255, 255), font=font_title)
        draw.text((x, curr_y + mobile_thumb_h + 32), "Codealytica  •  1.2K views  •  Day 01 Masterclass", fill=(170, 170, 170), font=font_meta)

        curr_y += item_h

    mobile_path = PREVIEWS_DIR / "mobile_feed_preview.png"
    preview.save(mobile_path, "PNG", optimize=True)
    logger.info(f"Generated Mobile Preview: {mobile_path}")
    return mobile_path


def generate_report(results: List[dict]) -> None:
    lines = [
        "# 🎨 Codealytica YouTube Thumbnail Generation Report",
        f"*Generated on: {os.path.basename(sys.argv[0])}*",
        "",
        "## 📌 Project Overview",
        "- **Brand:** `CODEALYTICA` (*CODE. ANALYZE. BUILD. GROW.*)",
        "- **Series:** Generative AI & LLM Engineering Masterclass (Day 01)",
        "- **Resolution:** `1280 × 720` (16:9 Standard)",
        "- **Output Directory:** [`D:\\Codealytica\\YouTube_Publisher\\Thumbnail_Generator\\output`](file:///d:/Codealytica/YouTube_Publisher/Thumbnail_Generator/output)",
        "- **Contact Sheet:** [`D:\\Codealytica\\YouTube_Publisher\\Thumbnail_Generator\\previews\\contact_sheet_all_six.png`](file:///d:/Codealytica/YouTube_Publisher/Thumbnail_Generator/previews/contact_sheet_all_six.png)",
        "- **Mobile Feed Preview:** [`D:\\Codealytica\\YouTube_Publisher\\Thumbnail_Generator\\previews\\mobile_feed_preview.png`](file:///d:/Codealytica/YouTube_Publisher/Thumbnail_Generator/previews/mobile_feed_preview.png)",
        "",
        "## 📊 Thumbnail Verification & QA Matrix",
        "",
        "| # | Video ID | Headline | Supporting Subtitle | Dimensions | File Size | QA Result | Output File |",
        "|---|----------|----------|----------------------|------------|-----------|-----------|-------------|",
    ]

    for r in results:
        v = r["validation"]
        status_icon = "✅ PASSED" if v["overall_valid"] else "❌ FAILED"
        clean_path = r['file_path'].replace('\\', '/')
        lines.append(
            f"| {r['lesson_num']:02d} | `{r['video_id']}` | **{r['headline']}** | {r['supporting']} | {v['width']}x{v['height']} | {v['file_size_mb']} MB | {status_icon} | [`{r['filename']}`](file:///{clean_path}) |"
        )

    lines.extend([
        "",
        "## 🎯 Design Concepts & CTR Strategy",
        "",
        "### 1. Lesson 01 (`zP0kOyucuMA`) — RUN AI LOCALLY!",
        "- **Hook:** `NO CLOUD. NO COST.` + `ZERO CLOUD COST` badge.",
        "- **Visual:** Real PowerShell automation terminal installing Ollama on Windows with live download progress.",
        "- **Audience Rationale:** Eliminates friction and hesitation around cloud GPU bills and API tokens.",
        "",
        "### 2. Lesson 02 (`x-7RglvLPVw`) — 2 BILLION PARAMETERS?!",
        "- **Hook:** `GEMMA 2B EXPLAINED` + `GOOGLE GEMMA` badge.",
        "- **Visual:** Real terminal pulling 3.5 GB Gemma 2B manifest with successful model verification + 2B parameter architecture callout.",
        "- **Audience Rationale:** Creates an instant curiosity gap about what billions of parameters actually represent in practice.",
        "",
        "### 3. Lesson 03 (`v0Ce7IYYCvU`) — ONLY 8GB RAM?!",
        "- **Hook:** `RUN LOCAL AI` + `8GB LAPTOP READY` badge.",
        "- **Visual:** Real Qwen 2.5 0.5B lightweight model download (394 MB) executing on modest laptop specs.",
        "- **Audience Rationale:** Empowers developers who do not have high-end gaming laptops or cloud subscriptions.",
        "",
        "### 4. Lesson 04 (`bUsxJjJW0uY`) — WATCH YOUR GPU!",
        "- **Hook:** `AI PERFORMANCE TEST` + `LIVE GPU BENCHMARK` badge.",
        "- **Visual:** Real Windows Task Manager Performance dashboard displaying CPU spikes, Intel UHD and NVIDIA GeForce GTX telemetry.",
        "- **Audience Rationale:** High-energy visual confirmation that models actually use local hardware efficiently.",
        "",
        "### 5. Lesson 05 (`ThBJnBpSjkI`) — SMALL vs LARGE AI",
        "- **Hook:** `WHICH MODEL WINS?` + `THE STAR ANALOGY` badge.",
        "- **Visual:** Side-by-side comparison cards (Compact 0.5B vs Massive 70B) with the Star Analogy.",
        "- **Audience Rationale:** Contrasts efficiency vs capacity to guide proper architectural choices.",
        "",
        "### 6. Lesson 06 (`EjkFaIYaU60`) — AI: 3 GOLDEN RULES",
        "- **Hook:** `KNOW THIS FIRST!` + `DAY 01 FINALE` badge.",
        "- **Visual:** High-contrast conclusion visual framing the 3 foundational rules before advancing to Day 02.",
        "- **Audience Rationale:** Signals structured progression and strong finish for course retention.",
        "",
        "---",
        "*Report automatically generated by Codealytica Thumbnail Pipeline*",
    ])

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logger.info(f"Generated Generation Report: {REPORT_PATH}")


def main():
    if not CONFIG_PATH.exists():
        logger.error(f"Configuration file not found: {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    composer = EnhancedThumbnailComposer(config)
    results = []
    generated_thumbnails = []

    logger.info(f"Generating {len(config['thumbnails'])} enhanced thumbnails...")

    for item in config["thumbnails"]:
        num = item["lesson_num"]
        vid = item["video_id"]
        logger.info(f"Rendering Thumbnail {num:02d}: {item['headline']} ({vid})...")

        img = composer.compose_thumbnail(item)

        filename = f"Lesson_{num:02d}_{vid}_Thumbnail.png"
        out_path = OUTPUT_DIR / filename
        img.save(out_path, "PNG", optimize=True)

        validation = validate_thumbnail(img, out_path)
        logger.info(f"  -> Saved {out_path.name} ({validation['file_size_mb']} MB, valid={validation['overall_valid']})")

        results.append({
            "lesson_num": num,
            "video_id": vid,
            "headline": item["headline"],
            "supporting": item["supporting_text"],
            "filename": filename,
            "file_path": str(out_path),
            "validation": validation,
        })
        generated_thumbnails.append((item, img))

    contact_path = create_contact_sheet(generated_thumbnails)
    mobile_path = create_mobile_preview(generated_thumbnails)
    generate_report(results)

    print("\n" + "=" * 75)
    print("🎉 ENHANCED THUMBNAIL GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 75)
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Contact Sheet:    {contact_path}")
    print(f"Mobile Preview:   {mobile_path}")
    print(f"Report:           {REPORT_PATH}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()

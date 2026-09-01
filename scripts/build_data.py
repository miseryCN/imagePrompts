#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan image/ and video/ directories for Markdown prompt files,
detect associated media assets, calculate the exact closest standard aspect ratio,
and generate data/prompts.json and data/prompts.js with automatic cache-busting timestamp versioning.
"""

import os
import re
import time
import json
from pathlib import Path
from PIL import Image

STANDARD_RATIOS = [
    ("21:9", 21 / 9),
    ("16:9", 16 / 9),
    ("3:2",  3 / 2),
    ("4:3",  4 / 3),
    ("1:1",  1 / 1),
    ("3:4",  3 / 4),
    ("2:3",  2 / 3),
    ("9:16", 9 / 16),
    ("9:21", 9 / 21),
]

CATEGORY_NAMES = {
    "image": {
        "_label": "图像生成",
        "_icon": "image",
        "portrait": "人像写真",
        "landscape": "风光场景",
        "anime": "动漫二次元",
        "cg-fantasy": "CG与奇幻",
        "commercial": "商业电商",
        "artistic": "艺术风格",
    },
    "video": {
        "_label": "视频生成",
        "_icon": "video",
        "portrait": "人物动态",
        "cinematic": "电影运镜",
        "commercial": "商业广告",
        "nature": "自然风光",
        "vfx": "特效与概念",
    }
}

def calculate_closest_ratio(width: int, height: int) -> str:
    """Calculate the closest standard aspect ratio for given width and height."""
    if not width or not height or height == 0:
        return "16:9"
    actual_ratio = width / height
    closest = min(STANDARD_RATIOS, key=lambda x: abs(actual_ratio - x[1]))
    return closest[0]

def parse_markdown_file(file_path: Path, root_dir: Path):
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    rel_path = file_path.relative_to(root_dir).as_posix()
    parts = rel_path.split('/')
    if len(parts) < 3:
        return None
    
    cat = parts[0]
    subcat = parts[1]
    filename = parts[-1]

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = file_path.stem.replace('_', ' ')

    # Extract prompt text
    prompt_match = re.search(r'```(?:text|prompt)?\s*\n(.*?)\n```', content, re.DOTALL)
    if prompt_match:
        prompt_text = prompt_match.group(1).strip()
    else:
        prompt_text = ""

    # Extract metadata fields
    models = []
    models_match = re.search(r'推荐模型[^\n：:]*[：:]\s*([^\n]+)', content)
    if models_match:
        models_str = models_match.group(1).strip()
        models = [m.strip() for m in re.split(r'[/,、|]', models_str) if m.strip()]

    target_desc = ""
    target_match = re.search(r'生成目标[^\n：:]*[：:]\s*([^\n]+)', content)
    if target_match:
        target_desc = target_match.group(1).strip()

    # Detect associated media file
    media_url = ""
    media_type = cat # "image" or "video"
    actual_width = 0
    actual_height = 0
    aspect_ratio = ""

    stem = file_path.stem
    parent_dir = file_path.parent
    
    # 1. Search for matching image
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        cand = parent_dir / f"{stem}{ext}"
        if cand.exists():
            media_url = cand.relative_to(root_dir).as_posix()
            media_type = "image"
            try:
                with Image.open(cand) as im:
                    actual_width, actual_height = im.size
                    aspect_ratio = calculate_closest_ratio(actual_width, actual_height)
            except Exception as e:
                print(f"Warning reading image size {cand}: {e}")
            break
    
    # 2. Search for matching video
    if not media_url:
        for ext in ['.mp4', '.webm', '.gif']:
            cand = parent_dir / f"{stem}{ext}"
            if cand.exists():
                media_url = cand.relative_to(root_dir).as_posix()
                media_type = "video"
                break

    # 3. Fallback placeholder if no media
    if not media_url:
        if cat == "video":
            media_url = "assets/placeholder-video.mp4"
            media_type = "video"
            aspect_ratio = "16:9"
        else:
            media_url = "assets/placeholder-image.jpg"
            media_type = "image"
            aspect_ratio = "4:3"

    # Fallback aspect ratio from markdown if not detected from image
    if not aspect_ratio:
        ar_match = re.search(r'(?:推荐画幅|比例|Aspect Ratio)[^\n：:]*[：:]\s*([^\n]+)', content)
        if ar_match:
            raw_ar = ar_match.group(1).strip()
            for std_name, _ in STANDARD_RATIOS:
                if std_name in raw_ar:
                    aspect_ratio = std_name
                    break
        if not aspect_ratio:
            aspect_ratio = "16:9" if cat == "video" else "3:4"

    cat_label = CATEGORY_NAMES.get(cat, {}).get("_label", cat)
    subcat_label = CATEGORY_NAMES.get(cat, {}).get(subcat, subcat)

    dimensions_str = f"{actual_width}x{actual_height}" if actual_width and actual_height else ""

    return {
        "id": rel_path.replace('/', '__').replace('.md', ''),
        "title": title,
        "category": cat,
        "categoryLabel": cat_label,
        "subcategory": subcat,
        "subcategoryLabel": subcat_label,
        "path": rel_path,
        "filename": filename,
        "target": target_desc or title,
        "models": models,
        "aspectRatio": aspect_ratio,
        "dimensions": dimensions_str,
        "prompt": prompt_text,
        "mediaType": media_type,
        "mediaUrl": media_url,
        "rawContent": content,
    }

def build_data():
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / "data"
    data_dir.mkdir(exist_ok=True)

    version_timestamp = str(int(time.time()))

    items = []
    for top_cat in ["image", "video"]:
        cat_dir = root_dir / top_cat
        if not cat_dir.exists():
            continue
        for md_file in cat_dir.rglob("*.md"):
            item = parse_markdown_file(md_file, root_dir)
            if item:
                items.append(item)

    output_data = {
        "version": version_timestamp,
        "categories": CATEGORY_NAMES,
        "total": len(items),
        "prompts": items
    }

    # Write prompts.json
    out_file = data_dir / "prompts.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # Write prompts.js for instant zero-latency loading
    js_file = data_dir / "prompts.js"
    with open(js_file, "w", encoding="utf-8") as f:
        f.write("window.STITCH_PROMPTS_DATA = " + json.dumps(output_data, ensure_ascii=False, indent=2) + ";\n")

    # Update index.html script tag with cache-busting version
    index_file = root_dir / "index.html"
    if index_file.exists():
        index_html = index_file.read_text(encoding="utf-8")
        updated_html = re.sub(
            r'<script\s+src="data/prompts\.js(?:\?v=[^"]*)?"',
            f'<script src="data/prompts.js?v={version_timestamp}"',
            index_html
        )
        index_file.write_text(updated_html, encoding="utf-8")

    print(f"Generated {out_file} and {js_file} with {len(items)} prompts (Version: {version_timestamp}).")
    return output_data

if __name__ == "__main__":
    build_data()

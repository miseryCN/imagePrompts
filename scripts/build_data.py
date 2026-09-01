#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan image/ and video/ directories for Markdown prompt files,
detect associated media assets (or assign defaults),
and generate data/prompts.json for the GitHub Pages static website.
"""

import os
import re
import json
from pathlib import Path

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

    aspect_ratio = ""
    ar_match = re.search(r'(?:推荐画幅|比例|Aspect Ratio)[^\n：:]*[：:]\s*([^\n]+)', content)
    if ar_match:
        aspect_ratio = ar_match.group(1).strip()

    # Detect custom media in same directory or frontmatter
    media_url = ""
    media_type = cat # "image" or "video"

    # Check if there is a matching image/video with same stem
    stem = file_path.stem
    parent_dir = file_path.parent
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        cand = parent_dir / f"{stem}{ext}"
        if cand.exists():
            media_url = cand.relative_to(root_dir).as_posix()
            media_type = "image"
            break
    
    if not media_url:
        for ext in ['.mp4', '.webm', '.gif']:
            cand = parent_dir / f"{stem}{ext}"
            if cand.exists():
                media_url = cand.relative_to(root_dir).as_posix()
                media_type = "video"
                break

    # Fallback placeholders
    if not media_url:
        if cat == "video":
            media_url = "assets/placeholder-video.mp4"
            media_type = "video"
        else:
            media_url = "assets/placeholder-image.jpg"
            media_type = "image"

    cat_label = CATEGORY_NAMES.get(cat, {}).get("_label", cat)
    subcat_label = CATEGORY_NAMES.get(cat, {}).get(subcat, subcat)

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
        "prompt": prompt_text,
        "mediaType": media_type,
        "mediaUrl": media_url,
        "rawContent": content,
    }

def build_data():
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / "data"
    data_dir.mkdir(exist_ok=True)

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
        "categories": CATEGORY_NAMES,
        "total": len(items),
        "prompts": items
    }

    out_file = data_dir / "prompts.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Generated {out_file} with {len(items)} prompts.")

    return output_data

if __name__ == "__main__":
    build_data()

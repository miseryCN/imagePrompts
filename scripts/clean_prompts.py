#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean, normalize, and format prompt text across all markdown files:
- Removes irregular copy-paste spacing and broken line wraps
- Formats structured tags (e.g. 核心主体/衣着搭配/场景环境/负面提示词) onto clean distinct lines
- Normalizes Chinese punctuation spacing
- Formats prompt blocks in Markdown cleanly
"""

import re
from pathlib import Path

SECTION_TAGS = [
    r'核心主体[：:]',
    r'衣着(?:搭配)?[：:]',
    r'表情[、与及]妆容[：:]',
    r'核心动作(?:/状态)?[：:]',
    r'动作设计[：:]',
    r'场景环境[：:]',
    r'镜头(?:焦段[、与]光圈[、与]景别|景别|语言)?[：:]',
    r'光照(?:方向[、与]强度|氛围)?[：:]',
    r'色彩风格[：:]',
    r'整体氛围[：:]',
    r'画质要求[：:]',
    r'画面呈现[“"”\']?',
    r'背景柔和虚化[：:]?',
    r'负面提示词[：:]?',
    r'人物特征[：:]',
    r'发型配饰[：:]',
    r'关键细节[：:]',
]

def clean_prompt_text(raw_text: str) -> str:
    if not raw_text:
        return ""

    text = raw_text.replace('\r\n', '\n').replace('\r', '\n')

    # Convert known section tags preceded by multiple spaces into a newline
    for tag in SECTION_TAGS:
        text = re.sub(rf'[ \t]{{2,}}({tag})', r'\n\1', text)

    # Normalize multiple spaces into single space
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        l = line.strip()
        if not l:
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
            continue

        # Replace multiple spaces with a single space
        l = re.sub(r'[ \t]{2,}', ' ', l)
        
        # Clean spacing around Chinese punctuation
        l = re.sub(r'([，。！？；：、（）]) +', r'\1', l)
        l = re.sub(r' +([，。！？；：、（）])', r'\1', l)

        cleaned_lines.append(l)

    # Collapse more than 2 consecutive blank lines
    result = '\n'.join(cleaned_lines).strip()
    return result

def clean_markdown_file(file_path: Path):
    content = file_path.read_text(encoding='utf-8')

    # Find the prompt block
    prompt_match = re.search(r'```(?:text|prompt)?\s*\n(.*?)\n```', content, re.DOTALL)
    if not prompt_match:
        return False

    raw_prompt = prompt_match.group(1)
    cleaned_prompt = clean_prompt_text(raw_prompt)

    if raw_prompt.strip() != cleaned_prompt:
        new_content = content[:prompt_match.start(1)] + cleaned_prompt + content[prompt_match.end(1):]
        file_path.write_text(new_content, encoding='utf-8')
        print(f"Cleaned prompt in: {file_path.name}")
        return True
    return False

def clean_all():
    root_dir = Path(__file__).resolve().parent.parent
    count = 0
    for md_file in root_dir.glob("*/**/*.md"):
        if clean_markdown_file(md_file):
            count += 1
    print(f"Finished formatting. Total updated files: {count}")

if __name__ == "__main__":
    clean_all()

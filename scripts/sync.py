#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All-in-one Prompt Repository Sync & Auto-Binding Manager.
- Auto-matches loose / UUID-named image/video files to markdown prompts in the same folder.
- Rebuilds data/prompts.json and data/prompts.js.
- Commits and pushes changes to GitHub.
"""

import sys
import subprocess
from pathlib import Path
from build_data import build_data

ROOT_DIR = Path(__file__).resolve().parent.parent

def auto_bind_media_files():
    """
    Search for stray image/video files in image/ and video/ subdirectories
    that do not match an existing markdown stem, and pair them with markdown files.
    """
    matched_count = 0
    for top_cat in ["image", "video"]:
        cat_dir = ROOT_DIR / top_cat
        if not cat_dir.exists():
            continue
        for sub_dir in cat_dir.iterdir():
            if not sub_dir.is_dir():
                continue
            
            md_files = list(sub_dir.glob("*.md"))
            media_files = [f for f in sub_dir.iterdir() if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".mp4", ".webm", ".gif"]]
            
            # Find markdown files that have no matching media
            unpaired_mds = []
            for md in md_files:
                stem = md.stem
                has_matching = any(f.stem == stem for f in media_files)
                if not has_matching:
                    unpaired_mds.append(md)
            
            # Find media files that have no matching markdown
            unpaired_media = []
            for m in media_files:
                stem = m.stem
                has_matching = any(md.stem == stem for md in md_files)
                if not has_matching:
                    unpaired_media.append(m)
            
            # If 1 unpaired md and 1 unpaired media in the folder, auto-pair them!
            if len(unpaired_mds) == 1 and len(unpaired_media) == 1:
                target_md = unpaired_mds[0]
                source_media = unpaired_media[0]
                new_media_path = source_media.parent / f"{target_md.stem}{source_media.suffix.lower()}"
                source_media.rename(new_media_path)
                print(f"[Auto-Bind] Paired: {source_media.name} -> {new_media_path.name}")
                matched_count += 1

    return matched_count

def git_commit_and_push(commit_msg: str = "chore: sync prompt repository and update showcase"):
    """Stage, commit and push all changes to GitHub main branch."""
    print("Staging changes...")
    subprocess.run(["git", "add", "-A"], cwd=ROOT_DIR, check=True)
    
    # Check if there are changes to commit
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT_DIR, capture_output=True, text=True)
    if not status.stdout.strip():
        print("No changes to commit. Repository is clean.")
        return False
    
    print(f"Committing with message: '{commit_msg}'...")
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=ROOT_DIR, check=True)
    
    print("Pushing to origin main...")
    subprocess.run(["git", "push", "origin", "main"], cwd=ROOT_DIR, check=True)
    print("Successfully synced and pushed to GitHub Pages!")
    return True

def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "feat: update prompt repository, media assets, and showcase index"
    
    print("=== [1/3] Checking & Auto-Binding Media Assets ===")
    auto_bind_media_files()
    
    print("\n=== [2/3] Rebuilding Prompts Index (JSON & JS) ===")
    build_data()
    
    print("\n=== [3/3] Git Sync & Push ===")
    git_commit_and_push(commit_msg)
    
    print("\nAll done! Online showcase: https://miserycn.github.io/imagePrompts/")

if __name__ == "__main__":
    main()

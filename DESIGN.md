---
name: Prompts Hub Design System
version: 2.0.0
author: AI Prompts Studio
description: A state-of-the-art, cinematic dark-mode design system tailored for AI image & video prompt curation, inspection, and rapid copying.
---

# 🎨 Prompts Hub - DESIGN.md

## 1. 视觉哲学 (Design Philosophy)
- **Deep Space Obsidian (深邃黑曜石)**：以极夜深空灰与黑曜石（`#05060A`, `#0B0E14`, `#121721`）作为视觉基底，摒弃平庸的纯灰底色。
- **Luminescent Accents (极光辉光)**：采用高饱和、高通透度的霓虹电光紫（`#8B5CF6`）、青绿（`#06B6D4`）、洋红（`#EC4899`）作为交互反馈与焦点高亮。
- **Linear / Raycast 精致微交互**：卡片光标追踪聚光灯（Spotlight）、平滑微弹性缓动、磨砂毛玻璃（Glassmorphism）、一键复制五彩纸屑微粒子动画。
- **Information Hierarchy (信息密度与层次)**：突出核心生成物与视觉特征，弱化辅助元数据，代码与 Prompt 采用等宽极客字体（JetBrains Mono）。

---

## 2. 核心设计令牌 (Design Tokens)

### 颜色系统 (Color Palette)
- **Background Deep**: `#040508` (主背景)
- **Surface Elevation 1**: `#0A0D14` (卡片/侧边栏)
- **Surface Elevation 2**: `#121824` (悬浮卡片/弹窗)
- **Border Subtle**: `rgba(255, 255, 255, 0.08)`
- **Border Highlight**: `rgba(139, 92, 246, 0.4)`
- **Primary Brand (Violet)**: `#8B5CF6` / `#7C3AED`
- **Cyan Accent (Cyberpunk)**: `#06B6D4`
- **Emerald Accent (Success)**: `#10B981`
- **Rose Accent (Highlight)**: `#F43F5E`

### 字体系统 (Typography)
- **Primary Text**: `'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Code & Prompts**: `'JetBrains Mono', 'Fira Code', Menlo, monospace`

---

## 3. 动效与交互标准 (Motion & Interactions)
- **库选型**：GSAP 3.x (GreenSock)、Canvas 交互粒子背景、Canvas-Confetti 纸屑爆炸反馈。
- **缓动曲线**：`power3.out`（快速响应、平滑减速）、`expo.out`（弹窗展开）。
- **Spotlight 效果**：鼠标移过卡片时，跟随指针产生 `radial-gradient` 边界微光与柔和泛光。
- **快捷键体验**：支持 `/` 快速搜索、`Esc` 退出弹窗、键盘 Tab / 方向键无障碍浏览。

---
name: Stitch Design System - Prompt Studio
version: 3.0.0
author: Stitch Design Studio
description: A high-precision, warm-charcoal editorial design system inspired by Google Labs Stitch & high-end creative tooling.
---

# 📐 DESIGN.md - Stitch Design System

## 1. 核心设计哲学 (Design Philosophy)
- **Warm Charcoal & Titanium (暖炭黑曜与钛金灰)**：告别廉价的高饱和度蓝紫霓虹渐变。采用纯净温润的深炭灰基底（`#0B0C0E`、`#13151A`、`#1A1D24`），配合温润纸白（`#F8FAFC`）与暖色调。
- **Analog Precision & Terracotta Accent (陶土暖橙与精工细节)**：以代表创意活力与工业精密感的陶土暖橙（`#E25B36`）与琥珀金（`#F59E0B`）为主交互焦点，点缀鼠尾草青绿（`#14B8A6`）。
- **Media-First Showcase (成图与成片第一原则)**：每个提示词卡片及详情弹窗均留出高规格的真实素材画幅（Image Viewport / Video Player），无缝展示实际生成的最终产物与动态成片。
- **Tactile Editorial Layout (杂志级排版与微触感)**：利用发丝线（Hairline Borders）、等宽技术标签（JetBrains Mono）、纯粹的排版节奏与精巧的微交互。

---

## 2. 核心设计令牌 (Tokens)

### 颜色系统 (Color Palette)
- **Background Base**: `#08090C` (极深暖炭)
- **Surface Elevation 1**: `#101217` (卡片/侧边栏)
- **Surface Elevation 2**: `#181B22` (悬浮卡片/弹窗)
- **Border Hairline**: `rgba(255, 255, 255, 0.08)`
- **Border Focused**: `rgba(226, 91, 54, 0.5)`
- **Primary Accent (Terracotta/Flame)**: `#E25B36` / `#F06E47`
- **Secondary Accent (Amber Gold)**: `#F59E0B`
- **Video Motion Accent (Sage Teal)**: `#14B8A6`
- **Text Primary**: `#F8FAFC`
- **Text Muted**: `#94A3B8` / `#64748B`

### 字体系统 (Typography)
- **Headings**: `'Plus Jakarta Sans', system-ui, sans-serif` (700 / 800)
- **Mono / Data / Prompts**: `'JetBrains Mono', 'Fira Code', monospace`

---

## 3. 素材展示规范 (Media Guidelines)
- **图片展示**：支持自适应画幅裁剪，悬浮微放大（Scale 1.03），支持点击进入高清单图检视。
- **视频展示**：原生 HTML5 Video 循环静音自动播放，支持全屏与控制条交互。
- **占位规范**：新添加提示词默认使用系统占位图/视频，后续放入同名图片或视频即可自动渲染真实成图成片。

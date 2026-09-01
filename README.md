# AI 提示词仓库 (Prompts Repository)

本仓库用于系统化收集、整理与沉淀各类 AI 提示词（Prompts）。

---

## 📁 目录分类规范

仓库按应用领域与模态使用文件夹进行分类：

- 🎨 [`image/`](image/)：图像生成提示词（Midjourney, Flux, Stable Diffusion, DALL-E 等）
- 🎬 [`video/`](video/)：视频生成提示词（MiniMax, Kling, Runway, Pika, Sora, Wan 等）
- 💻 [`code/`](code/)：代码与软件工程提示词（架构设计、代码生成、重构、审查等）
- ✍️ [`writing/`](writing/)：文案创作与文本生成（文章、文案、社媒排版、翻译等）
- 🤖 [`agent-system/`](agent-system/)：Agent 设定与系统提示词（角色设定、System Prompt、知识库交互等）
- 🎵 [`audio/`](audio/)：音频与声音生成提示词（配乐、音效、TTS 配音等）
- ⚡ [`workflow/`](workflow/)：复合工作流与结构化处理提示词（CoT 链式推理、结构化提取等）

---

## 📝 提示词文件规范

1. **单文件单提示词**：每个提示词必须为独立的 Markdown (`.md`) 文件。
2. **标题与命名**：
   - 文件名及文档一级标题（`#`）必须明确描述**该提示词所生成的目标产物/内容**。
   - 示例：`# 赛博朋克雨夜未来街道概念图.md`、`# React_Tailwind_响应式登录注册组件.md`。
3. **推荐文档模板**：

```markdown
# [目标产物名称：清晰写明该提示词生成什么]

## 1. 基本信息
- **适用场景**：[例如：UI/UX 设计、故事绘本、数据清洗等]
- **推荐模型/平台**：[例如：Midjourney v6 / Claude 3.7 Sonnet / Flux.1-dev]
- **版本/更新时间**：2026-09-01

## 2. 提示词内容 (Prompt)
\`\`\`text
[在此放置完整的提示词文本 / System Prompt / User Prompt]
\`\`\`

## 3. 推荐参数 / 配置 (可选)
- **Aspect Ratio / 比例**：--ar 16:9
- **Temperature**：0.7
- **Negative Prompt / 负向提示词**：...

## 4. 预期产出 / 效果示例 (可选)
- [简要说明预期产出效果或使用注意事项]
```

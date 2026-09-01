# wkmdog - 创意图像与视频提示词实验室

> 🎨 图像与 🎬 视频 AI 提示词库 | 在线展示：[https://miserycn.github.io/imagePrompts/](https://miserycn.github.io/imagePrompts/)

---

## 📁 目录分类规范

仓库专注于**图像生成（Image）**与**视频生成（Video）**两大领域，并在二级目录下进行细分类别：

### 🎨 图像生成 (`image/`)
- [`image/portrait/`](image/portrait/)：人像写真 / 商业肖像 / 模特人物
- [`image/landscape/`](image/landscape/)：自然风光 / 建筑场景 / 空间环境
- [`image/anime/`](image/anime/)：二次元 / 动漫插画 / 赛璐璐
- [`image/cg-fantasy/`](image/cg-fantasy/)：科幻CG / 奇幻插画 / 游戏概念设计
- [`image/commercial/`](image/commercial/)：电商静物 / 产品广告 / 商业海报
- [`image/artistic/`](image/artistic/)：艺术风格 / 油画水彩 / 抽象美学

### 🎬 视频生成 (`video/`)
- [`video/portrait/`](video/portrait/)：人物动态 / 舞蹈动作 / 情绪特写
- [`video/cinematic/`](video/cinematic/)：电影运镜 / 故事镜头 / 电影感场景
- [`video/commercial/`](video/commercial/)：产品展示 / 商业广告 / 宣传片
- [`video/nature/`](video/nature/)：自然风光 / 天气变化 / 动植物
- [`video/vfx/`](video/vfx/)：特效转场 / 概念视觉 / 创意动画

---

## 📝 提示词文件规范

1. **单文件单提示词**：每个提示词必须为独立的 Markdown (`.md`) 文件，放置在对应的二级分类目录下。
2. **命名与一级标题**：
   - 文件名及文档一级标题（`#`）必须明确描述**该提示词所生成的目标产物/内容**。
   - 示例：`# 户外网球场夏日清爽运动写真_年轻女性前倾撑膝人像.md`。
3. **标准文档结构**：
   - **标题**：清晰写明该提示词生成什么
   - **基本信息**：生成目标、适用模型、推荐画幅/参数
   - **提示词正文**：完整 Prompt 内容（代码块包裹）
   - **关键要素拆解 / 参数说明**：关键视觉点、光影质感、镜头语言等

---
name: prompt-submit
description: AI 提示词与配套图片/视频素材的规范化录入、自动绑定、画幅比例计算与一键发布流水线。当用户提供提示词文本、上传成图/成片素材、要求添加/更新提示词库、或同步到 GitHub Pages 时使用。
---

# 提示词与媒体素材提交发布工作流 (Prompt & Media Submission Workflow)

本 Skill 规范了向 `wkmdog` 提示词实验室（`imagePrompts`）提交新提示词、绑定图片/视频素材、自动计算标准画幅比例以及一键发布到 GitHub Pages 的标准作业流程。

---

## 1. 目录分类路由规范

根据提示词的目标产物类型与领域，将其路由至对应的一级和二级目录：

### 🎨 图像分类 (`image/`)
- `image/portrait/`：人像写真 / 商业肖像 / 模特人物 / 角色设定
- `image/landscape/`：自然风光 / 建筑场景 / 空间环境
- `image/anime/`：二次元 / 动漫插画 / 赛璐璐
- `image/cg-fantasy/`：科幻CG / 奇幻插画 / 游戏概念设计
- `image/commercial/`：电商静物 / 产品广告 / 商业海报
- `image/artistic/`：艺术风格 / 油画水彩 / 抽象美学

### 🎬 视频分类 (`video/`)
- `video/portrait/`：人物动态 / 舞蹈动作 / 情绪特写
- `video/cinematic/`：电影运镜 / 故事镜头 / 电影感场景
- `video/commercial/`：产品展示 / 商业广告 / 宣传片
- `video/nature/`：自然风光 / 天气变化 / 动植物
- `video/vfx/`：特效转场 / 概念视觉 / 创意动画

---

## 2. Markdown 提示词文件标准结构

在对应子目录下创建 `{描述性命名}.md`（文件名必须明确描述生成产物，例如 `古风汉服少女角色设定参考图_浅冰蓝齐腰襦裙拼贴版式.md`）。

> ⚠️ **重要规则**：
> - 严禁在 Markdown 或任何字段中包含「推荐模型」信息。
> - 提示词正文必须使用 ` ```text ` 或 ` ```prompt ` 代码块包裹。

### 模板示例：
```markdown
# {目标产物名称} - {特征副标题}

## 1. 基本信息
- **生成目标**：{详细描述生成画面或视频的目标}
- **分类**：`image` 或 `video` ({所属二级分类中文名})
- **推荐画幅**：{例如 9:16 / 3:4 / 1:1 / 4:3 / 16:9}
- **风格标签**：{关键词标签}

---

## 2. 提示词正文 (Prompt)

```text
{完整提示词内容}
```

---

## 3. 关键要素拆解 / 视觉特征
- **构图/镜头**：{构图方式与运镜说明}
- **主体/姿态**：{主体特征与动态设计}
- **光影/色彩**：{光照质感与色彩基调}
- **细节/材质**：{细节表现与微观特征}
```

---

## 3. 素材文件命名与绑定

- **同名配套原则**：素材文件与 `.md` 文件必须位于同一目录下，且主文件名完全一致（如 `example.md` 对应 `example.png` 或 `example.mp4`）。
- **支持格式**：
  - 图像：`.png`, `.jpg`, `.jpeg`, `.webp`
  - 视频：`.mp4`, `.webm`, `.gif`
- **自动绑定机制**：如果用户直接将图片丢入子目录（如 `UUID.png` 或 `screenshot.jpg`），无需手动重命名，运行 `scripts/sync.py` 会自动将该目录下未配对的图片与未配对的 `.md` 自动绑定。

---

## 4. 一键构建、比例计算与 Git 同步

在仓库根目录（`D:\soft\prompts`）执行一键同步命令：

```bash
python scripts/sync.py "feat: add {新提示词简述} prompt and media asset"
```

### 流水线内部执行逻辑：
1. **自动资产配对**：扫描并重命名匹配媒体文件。
2. **像素级比例计算**：通过 PIL 读取图片宽高，自动对齐最接近的标准比例（`21:9`, `16:9`, `3:2`, `4:3`, `1:1`, `3:4`, `2:3`, `9:16`, `9:21`）。
3. **索引生成与双重缓存失效**：生成 `data/prompts.json` 与 `data/prompts.js`，并注入全新 Unix 时间戳版本号，彻底杜绝浏览器缓存。
4. **Git 自动化发布**：自动执行 `git add .`、`git commit` 并 `git push origin main` 到 GitHub Pages。

---

## 5. 验收与交付

同步完成后，在回复中向用户提供：
- 提示词标题与自动识别出的画幅比例
- GitHub Pages 在线展示链接：`https://miserycn.github.io/imagePrompts/`
- 纯享模式直达链接：`https://miserycn.github.io/imagePrompts/#enjoy`

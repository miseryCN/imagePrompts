# wkmdog // 提示词实验室 (imagePrompts)

## 项目简介
静态部署在 GitHub Pages 上的 AI 创意图像与视频提示词资产库系统，支持纯享短视频刷剧模式、多种画幅比例自适应、一键复制、时间排序等功能。

- 线上展示地址: `https://miserycn.github.io/imagePrompts/`
- 纯享模式: `https://miserycn.github.io/imagePrompts/#enjoy`
- 仓库路径: `https://github.com/miseryCN/imagePrompts`

---

## 常用命令与流水线

### 1. 提交与同步提示词 (一键流水线)
当录入新提示词与图片/视频素材后，在项目根目录下执行：
```bash
python scripts/sync.py "feat: add {新提示词简述} prompt and media asset"
```
流水线自动执行：
1. 自动配对子目录下的同名/未绑定图片与 Markdown 文件
2. 文本清洗与格式化（消除多余空格与粘连换行）
3. 通过 PIL 计算像素精确比例（21:9, 16:9, 3:2, 4:3, 1:1, 3:4, 2:3, 9:16, 9:21）
4. 抓取时间戳并按最新优先（Newest First）重新生成 `data/prompts.json` 与 `data/prompts.js`
5. 自动 `git commit` 并 `git push origin main` 到 GitHub Pages

### 2. 手动构建索引与排版清洗
```bash
python scripts/build_data.py
python scripts/clean_prompts.py
```

---

## 规范与技能 (Skills)

项目已配置标准 Skill：`prompt-submit`，位于 `.claude/skills/prompt-submit/SKILL.md` 和 `.agents/skills/prompt-submit/SKILL.md`。

### 核心规则：
1. **分类路由**：
   - 图像: `image/portrait/`, `image/landscape/`, `image/anime/`, `image/cg-fantasy/`, `image/commercial/`, `image/artistic/`
   - 视频: `video/portrait/`, `video/cinematic/`, `video/commercial/`, `video/nature/`, `video/vfx/`
2. **严禁包含推荐模型**：不得在 Markdown 中出现「推荐模型」相关字段。
3. **格式化排版**：提示词中的结构化标签（如 `核心主体：`、`场景环境：`、`负面提示词：` 等）必须分行排布，禁止杂乱粘连。

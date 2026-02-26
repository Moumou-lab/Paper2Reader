# Paper2Reader (P2R)

> 面向组会场景的论文自动解析与 Markdown 报告生成工具

## 项目简介

Paper2Reader 输入一篇 PDF 论文，自动完成：

- 论文文本抽取（逐页）
- 结构化解析（章节骨架 + 字段补充）
- 组会报告生成（Markdown）
- 论文图片抽取与图标题（caption）识别

当前版本已经能把 PDF 中的图片与 `captions.json` 一并输出，并将 captions 传入 Compose 阶段用于插图生成。

---

## 系统流程

```text
PDF 输入
  ↓
[1] 文本提取（utils/pdf_util.py）
  ↓
[2] MentorAgent 章节骨架提取（可选）
  ↓
[3] ParserAgent 工具调用增量补充 parser_paper
  ↓
[4] 图片抽取 + caption 匹配（captions.json）
  ↓
[5] ComposeAgent 生成 report.md（可插图）
```

---

## 核心能力

### 1) 多智能体解析

- `MentorAgent`：抽取章节骨架（标题层级）
- `ParserAgent`：结合工具 `recall/update` 逐页补充结构化字段
- `ComposeAgent`：基于 `parser_paper + captions` 生成组会报告

### 2) 工具调用（Function Calling）

- `tool_recall_sections`：按标题召回顶层 section
- `tool_update_sections`：按顶层标题回写更新后的 section

### 3) 图片抽取与图标题识别

`utils/pdf_util.py` 中已实现：

- `extract_pdf_images_with_captions(pdf_path, search_margin=140.0)`
  - 抽取 PDF 位图到 `outputs/<paper>/images/`
  - 为每张图片匹配附近最可能的 caption（优先下方、兼顾上方）
  - 自动落盘 `outputs/<paper>/images/captions.json`

返回字段示例：

- `image_path`, `relative_path`
- `page`, `index`, `xref`
- `width`, `height`, `bbox`
- `caption`, `caption_confidence`

---

## 目录说明

```text
Paper2Reader/
├── main.py
├── workflow.py
├── p2r_agents/
│   ├── compose_agent.py
│   ├── mentor_agent.py
│   ├── parser_agent.py
│   ├── prompts/
│   └── tools/
├── utils/
│   ├── json_util.py
│   └── pdf_util.py
└── outputs/
    └── <paper_name>/
        ├── parser_paper.json
        ├── report.md
        └── images/
            ├── p3_i1_x70.png
            └── captions.json
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

如本地缺少 `fitz`，请额外安装：

```bash
pip install pymupdf
```

### 2. 运行主流程

```bash
python main.py
```

默认输入论文路径在 `main.py` 中配置（`PDF_PATH`）。

### 3. 单独测试图片抽取

```python
from utils.pdf_util import extract_pdf_images_with_captions

items = extract_pdf_images_with_captions("papers/DSSM.pdf")
print(len(items), items[0]["caption"] if items else "no image")
```

---

## 输出产物

对论文 `papers/DSSM.pdf`，默认生成：

- `outputs/DSSM/parser_paper.json`
- `outputs/DSSM/images/*.png`
- `outputs/DSSM/images/captions.json`
- `outputs/DSSM/report.md`

---

## 配置说明

模型与 API 配置位于 `p2r_agents/config.py`，建议使用环境变量：

```python
BASE_URL = os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
TEXT_MODEL = "Pro/deepseek-ai/DeepSeek-V3.2"
```

---

## 开发进度

- [x] PDF 文本提取
- [x] 章节骨架提取（MentorAgent）
- [x] 逐页结构化补充（ParserAgent + tools）
- [x] Markdown 报告生成（ComposeAgent）
- [x] PDF 图片抽取
- [x] 图片 caption 识别与 `captions.json` 落盘
- [x] Compose 阶段接入 captions 插图信息
- [ ] PPT 自动生成

---

## License

MIT License
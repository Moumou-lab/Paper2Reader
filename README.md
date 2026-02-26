# Paper2Reader (P2R)

> 基于多智能体协作的学术论文自动解析与报告生成系统

## 📖 项目简介

Paper2Reader 旨在帮助研究生高效准备组会报告。输入 PDF 格式的学术论文，系统通过多智能体协作自动解析论文结构、提取关键内容，最终生成高质量的会议报告（含图表）。

核心设计理念：
- **Agentic Workflow**：多智能体自编排流程
- **上下文压缩**：逐步解析，避免超长上下文导致论文解读时的“幻觉/胡言乱语”
- **工具增强**：支持章节召回、内容补充等工具调用

---

## 🏗️ 系统架构

### 核心智能体

| 智能体 | 职责 | 特点 |
|--------|------|------|
| **MentorAgent** | 通用任务处理，章节骨架提取 | 基础 LLM 能力，全文理解 |
| **ParserAgent** | 论文逐页精细解析 | 结构化输出，增量更新 |
| **ComposeAgent** | 基于 `parser_paper` 生成组会 Markdown 报告 | 面向汇报场景的结构化写作 |
| **TestingAgent** | 工具调用测试与验证 | 支持 Function Calling |

### 工作流程

```
PDF 输入
  ↓
[1] PDF 文本提取（逐页）
  ↓
[2] MentorAgent 提取章节骨架（标题结构）
  ↓
[3] ParserAgent 工具化逐页召回目标 Sections 更新
  ↓
[4] 生成结构化 JSON（章节 + 子章节 + 内容）
  ↓
[5] ComposeAgent 基于 parser_paper 生成 Markdown 报告（`report.md`）
```

---

## 📦 核心模块

### 1. 智能体模块 (`p2r_agents/`)
- `mentor_agent.py`：通用 AI 助手，处理全局任务
- `parser_agent.py`：论文解析专家，支持工具调用循环（Function Calling + 回写）
- `compose_agent.py`：报告写作助手，基于 `parser_paper` 生成 Markdown
- `testing_agent.py`：工具调用测试，支持 Function Calling 循环
- `config.py`：统一的模型与 API 配置

### 2. 工具系统 (`p2r_agents/tools/`)
- `tool_schema.py`：工具函数的 JSON Schema 定义
- `parser_tool.py`：
  - `tool_recall_sections`：按标题召回顶层 section 完整 parser（命中 subsection 也返回所属顶层）
  - `tool_update_sections`：按顶层 `section_title` 匹配并回写更新结果

### 3. 提示词管理 (`p2r_agents/prompts/`)
- `mentor_prompt.py`：MentorAgent 的系统提示词
- `parser_prompt.py`：ParserAgent 的任务提示词
- `compose_prompt.py`：ComposeAgent 的系统提示词与报告任务提示词

### 4. 工具函数 (`utils/`)
- `pdf_util.py`：PDF 信息提取、文本解析
- `json_util.py`：结构化 JSON 读写与更新

---

## 🚀 使用方式

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行主流程
```bash
python main.py
```

### 测试单个智能体
```bash
# 测试 MentorAgent
python -m p2r_agents.mentor_agent

# 测试 TestingAgent（工具调用）
python -m p2r_agents.testing_agent
```

### 当前关键约定（已实现）
- 模型侧不感知 `pdf_path`，避免 prompt 污染。
- `pdf_path` 由 Agent 运行时注入到工具参数中（宿主代码注入上下文）。
- `parser_paper.json` 仍按 `outputs/{paper_name}/parser_paper.json` 管理。
- `workflow.py` 最后一步会生成 `outputs/{paper_name}/report.md`。

---

## 📊 开发进度

- [x] PDF 文本提取模块
- [x] MentorAgent 章节骨架提取
- [x] ParserAgent 工具化逐页补充（召回 + 回写）
- [x] 工具调用系统（Function Calling）
- [x] 结构化 JSON 输出
- [x] Markdown 报告生成（ComposeAgent）
- [ ] 图表提取与解析
- [ ] PPT 报告渲染
- [ ] 交互式问答优化, ToolCallling Retrieval 补充对点目标信息
- [ ] 多轮对话记忆管理

---

## 📝 配置说明

在 `p2r_agents/config.py` 中配置 API 密钥：

```python
BASE_URL = "https://api.siliconflow.cn/v1"
API_KEY = "your-api-key"  # 建议通过环境变量设置
TEXT_MODEL = "Pro/deepseek-ai/DeepSeek-V3.2"
```

---

## 📄 License

MIT License

---

**Status**: 🚧 Parsing + Markdown Reporting 已打通，持续迭代中
# Paper2Reader

一个基于多 Agent 工作流的论文阅读和笔记生成系统。输入一篇论文，自动生成结构化的笔记文档。

## 功能特点

- 🤖 **多 Agent 协作**：使用 4 个专业 Agent 协同工作
  - **Parser Agent**：解析论文结构和提取关键信息
  - **Semantic Agent**：进行深入的语义分析和理解
  - **Quality Agent**：质量检查和优化
  - **Output Agent**：生成最终的 Markdown 格式笔记
- 📝 **结构化输出**：生成包含摘要、贡献、方法、实验等完整结构的笔记
- 🔄 **自动工作流**：一键处理，自动完成从论文到笔记的转换
- ✅ **质量保证**：内置质量检查机制，确保笔记的完整性和准确性

## 项目结构

```
Paper2Reader/
├── agents/                  # Agent 模块
│   ├── base_agent.py        # 基础 Agent 类
│   ├── parser_agent.py      # 论文解析 Agent
│   ├── semantic_agent.py    # 语义分析 Agent
│   ├── quality_agent.py     # 质量检查 Agent
│   ├── output_agent.py      # 输出生成 Agent
│   ├── config.py            # 配置文件（API 密钥等）
│   └── prompts/             # 提示词模板
│       ├── parser_prompt.py
│       ├── semantic_prompt.py
│       ├── quality_prompt.py
│       └── output_prompt.py
├── papers/                  # 输入论文目录
├── outputs/                 # 输出笔记目录
├── workflow.py              # 工作流协调器
├── utils.py                 # 工具函数
├── main.py                  # 主入口文件
└── requirements.txt         # 依赖包

```

## 安装

1. 克隆或下载项目

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置 API 密钥：
编辑 `agents/config.py`，设置你的 ModelScope API 密钥和基础 URL。

## 使用方法

### 基本用法

从文件读取论文并生成笔记：
```bash
python main.py papers/your_paper.md
```

指定输出路径：
```bash
python main.py papers/your_paper.md -o outputs/my_note.md
```

直接输入论文文本：
```bash
python main.py "论文内容..." -t
```

列出可用的论文文件：
```bash
python main.py --list
```

### 工作流程

1. **Parser Agent** 解析论文，提取：
   - 标题、作者、摘要
   - 章节结构
   - 主要贡献
   - 方法论概述
   - 实验结果
   - 结论

2. **Semantic Agent** 进行语义分析：
   - 核心概念提取
   - 研究问题识别
   - 方法论深入分析
   - 关键洞察提取
   - 优缺点分析
   - 未来工作方向

3. **Quality Agent** 质量检查：
   - 完整性评分
   - 准确性评分
   - 清晰度评分
   - 缺失信息识别
   - 改进建议

4. **Output Agent** 生成最终笔记：
   - 结构化的 Markdown 文档
   - 包含所有关键信息
   - 易于阅读和参考

## 输出格式

生成的笔记包含以下部分：

- 基本信息（作者、关键词等）
- 摘要
- 核心贡献
- 研究方法
- 核心概念
- 研究问题
- 技术细节
- 实验结果
- 关键洞察
- 优点与局限性
- 实际应用
- 未来工作
- 结论

## 配置说明

在 `agents/config.py` 中配置：

- `BASE_URL`：ModelScope API 基础 URL
- `API_KEY`：你的 API 密钥
- 模型名称：默认使用 `deepseek-ai/DeepSeek-V3.2`

## 注意事项

- 确保论文文件是 UTF-8 编码的文本格式（.md, .txt）
- PDF 文件需要先转换为文本格式
- 处理长论文时可能需要较长时间
- API 调用会产生费用，请注意使用量

## 开发

### 添加新的 Agent

1. 继承 `BaseAgent` 类
2. 实现 `process()` 方法
3. 在 `workflow.py` 中集成到工作流

### 自定义提示词

编辑 `agents/prompts/` 目录下的提示词模板文件。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

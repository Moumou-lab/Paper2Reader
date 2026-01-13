# 快速开始指南

## 1. 安装依赖

```bash
# 进入项目目录
cd /Users/zhengjiaqi/Projects/Paper2Reader

# 安装 Python 依赖
pip install -r requirements.txt
```

## 2. 配置 API（如果需要）

如果你的 ModelScope API 密钥不同，编辑 `agents/config.py`：

```python
BASE_URL='https://api-inference.modelscope.cn/v1'
API_KEY='你的API密钥'
```

## 3. 准备论文文件

将论文文件（.md 或 .txt 格式）放入 `papers/` 目录。

**注意**：当前版本仅支持文本格式文件（.md, .txt）。如果是 PDF 文件，需要先转换为文本格式。

## 4. 运行

### 查看可用论文文件

```bash
python main.py
# 或
python main.py --list
```

### 处理论文（使用文件名）

```bash
# 直接使用文件名（推荐）
python main.py temp.md

# 如果文件名有空格，用引号括起来
python main.py "my paper.md"
```

### 处理论文（使用完整路径）

```bash
# 使用相对路径
python main.py papers/temp.md

# 使用绝对路径
python main.py /path/to/your/paper.md
```

### 直接输入文本内容

```bash
python main.py "论文内容..." -t
```

### 指定输出路径

```bash
python main.py temp.md -o outputs/my_note.md
```

## 5. 运行示例

项目包含一个示例脚本，可以直接运行：

```bash
python example.py
```

## 输出

处理完成后，笔记会自动保存到 `outputs/` 目录，文件名基于论文标题生成。

## 常见问题

### Q: 支持 PDF 文件吗？
A: 当前版本仅支持文本格式（.md, .txt）。PDF 文件需要先转换为文本格式。

### Q: 如何转换 PDF 为文本？
A: 可以使用以下工具：
- 在线工具：将 PDF 内容复制粘贴到 .md 文件
- Python 库：`pypdf2` 或 `pdfplumber`
- 命令行工具：`pdftotext`（需要安装 poppler）

### Q: 处理失败怎么办？
A: 
1. 检查 API 密钥是否正确
2. 检查论文文件是否可读
3. 查看错误日志信息
4. 可以尝试重新运行（系统支持自动重试）

### Q: 笔记保存在哪里？
A: 默认保存在 `outputs/` 目录，文件名格式为：`{论文标题}_note.md`

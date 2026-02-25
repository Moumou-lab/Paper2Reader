

TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "tool_recall_sections",
            "description": "根据标题列表召回章节内容, section或subsection的标题都接受",
            "parameters": {
                "type": "object",
                "properties": {
                    "titles": {
                        "type": "array",
                        "description": "章节标题列表",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["titles"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_update_sections",
            "description": "将补全后的顶层section完整parser回写到原文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "updated_sections": {
                        "type": "array",
                        "description": "待回写的顶层 section 完整 parser 列表",
                        "items": {
                            "type": "object"
                        }
                    }
                },
                "required": ["updated_sections"]
            }
        }
    },

]
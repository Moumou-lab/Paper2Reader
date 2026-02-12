

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

]
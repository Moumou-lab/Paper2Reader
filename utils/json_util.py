import json
from typing import List, Dict
from pathlib import Path



def _get_parser_json_path(pdf_path: str) -> Path:
    paper_name = Path(pdf_path).stem
    output_dir = Path("outputs") / paper_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / "parser_paper.json"


def read_parser_json(pdf_path: str) -> Dict:
    output_file = _get_parser_json_path(pdf_path)
    return json.loads(output_file.read_text(encoding="utf-8"))


def update_parser_json(pdf_path: str, section_outline: List[Dict]):
    output_file = _get_parser_json_path(pdf_path)
    output_file.write_text(
        json.dumps(section_outline, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_json_list(raw_text: str) -> List[Dict]:
    data = json.loads(raw_text)
    if not isinstance(data, list):
        raise ValueError("模型输出不是 JSON list")
    return data
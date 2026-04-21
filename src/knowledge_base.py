from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class KBChunk:
    title: str
    content: str


class KnowledgeBase:
    def __init__(self, path: str):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Knowledge base not found at: {self.path}")
        self.raw_text = self.path.read_text(encoding="utf-8")
        self.chunks = self._split_sections(self.raw_text)

    @staticmethod
    def _split_sections(markdown_text: str) -> list[KBChunk]:
        sections = re.split(r"^##\s+", markdown_text, flags=re.MULTILINE)
        chunks: list[KBChunk] = []
        for section in sections:
            section = section.strip()
            if not section:
                continue
            lines = section.splitlines()
            title = lines[0].strip("# ")
            content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
            chunks.append(KBChunk(title=title, content=content))
        return chunks

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

@dataclass(slots=True)
class AIRequest:
    url: str
    source_domain: Optional[str] = None
    title: Optional[str] = None
    meta_description: Optional[str] = None
    visible_text: Optional[str] = None
    schema_data: Optional[str] = None
    open_graph_data: Optional[str] = None
    max_input_chars: int = 12000
    requested_fields: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def build_context(self) -> str:
        chunks = []
        if self.url:
            chunks.append(f"URL:\n{self.url}")
        if self.title:
            chunks.append(f"TITLE:\n{self.title}")
        if self.meta_description:
            chunks.append(f"META DESCRIPTION:\n{self.meta_description}")
        if self.schema_data:
            chunks.append(f"SCHEMA:\n{self.schema_data}")
        if self.open_graph_data:
            chunks.append(f"OPEN GRAPH:\n{self.open_graph_data}")
        if self.visible_text:
            chunks.append(f"VISIBLE TEXT:\n{self.visible_text[:self.max_input_chars]}")
        return "\n\n".join(chunks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "source_domain": self.source_domain,
            "title": self.title,
            "meta_description": self.meta_description,
            "visible_text": self.visible_text,
            "schema_data": self.schema_data,
            "open_graph_data": self.open_graph_data,
            "max_input_chars": self.max_input_chars,
            "requested_fields": self.requested_fields,
            "metadata": self.metadata,
        }

    @property
    def has_content(self) -> bool:
        return bool(
            self.title
            or self.meta_description
            or self.visible_text
            or self.schema_data
            or self.open_graph_data
        )

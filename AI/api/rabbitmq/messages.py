from dataclasses import dataclass
from typing import Optional

@dataclass
class AIRequest:
    jobId: str
    prompt: str
    type: str # e.g., "chat", "upload"

@dataclass
class AIResponse:
    jobId: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None

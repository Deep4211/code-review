from pydantic import BaseModel
from typing import List, Optional

class CodeFile(BaseModel):
    filename: str
    content: str

class Issue(BaseModel):
    line: int
    type: str
    description: str

class Observation(BaseModel):
    pr_id: int
    files: List[CodeFile]
    step_count: int
    max_steps: int

class SingleAction(BaseModel):
    action_type: str  # comment | approve | request_changes
    line: Optional[int] = None
    comment: Optional[str] = None

class Action(BaseModel):
    actions: List[SingleAction]

class Reward(BaseModel):
    score: float
    reason: str

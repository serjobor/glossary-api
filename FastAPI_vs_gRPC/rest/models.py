from pydantic import BaseModel
from typing import Optional

class Term(BaseModel):
  title: str
  definition: str
  source_link: Optional[str] = None

class TermUpdate(BaseModel):
  definition: str
  source_link: Optional[str] = None
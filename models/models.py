from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    query: str
    history: Optional[List[Dict[str, str]]] = None


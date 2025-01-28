from pydantic import BaseModel
from typing import Optional, List

class RelationshipBase(BaseModel):
    source_term_id: int
    target_term_id: int
    relation_type: Optional[str] = None

class RelationshipCreate(RelationshipBase):
    pass

class Relationship(RelationshipBase):
    id: int
    class Config:
        orm_mode = True

class TermBase(BaseModel):
    name: str
    definition: str
    source: Optional[str] = None

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    name: Optional[str] = None
    definition: Optional[str] = None
    source: Optional[str] = None

class Term(TermBase):
    id: int
    outgoing_relationships: List[Relationship] = []
    incoming_relationships: List[Relationship] = []
    class Config:
        orm_mode = True

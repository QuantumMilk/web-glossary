from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    definition = Column(String, nullable=False)
    source = Column(String, nullable=True)

    outgoing_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.source_term_id",
        cascade="all, delete-orphan",
        back_populates="source_term",
    )
    incoming_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.target_term_id",
        cascade="all, delete-orphan",
        back_populates="target_term",
    )


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)
    source_term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)
    target_term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)
    relation_type = Column(String, nullable=True)

    source_term = relationship("Term", foreign_keys=[source_term_id], back_populates="outgoing_relationships")
    target_term = relationship("Term", foreign_keys=[target_term_id], back_populates="incoming_relationships")

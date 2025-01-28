from sqlalchemy.orm import Session
from . import models, schemas

# ---------- CRUD для Term ----------

def create_term(db: Session, term: schemas.TermCreate):
    db_term = models.Term(
        name=term.name,
        definition=term.definition,
        source=term.source
    )
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def get_term(db: Session, term_id: int):
    return db.query(models.Term).filter(models.Term.id == term_id).first()

def get_term_by_name(db: Session, name: str):
    return db.query(models.Term).filter(models.Term.name == name).first()

def get_terms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Term).offset(skip).limit(limit).all()

def update_term(db: Session, term_db: models.Term, updates: schemas.TermUpdate):
    if updates.name is not None:
        term_db.name = updates.name
    if updates.definition is not None:
        term_db.definition = updates.definition
    if updates.source is not None:
        term_db.source = updates.source
    db.commit()
    db.refresh(term_db)
    return term_db

def delete_term(db: Session, term_db: models.Term):
    db.delete(term_db)
    db.commit()

# ---------- CRUD для Relationship ----------

def create_relationship(db: Session, rel: schemas.RelationshipCreate):
    db_rel = models.Relationship(
        source_term_id=rel.source_term_id,
        target_term_id=rel.target_term_id,
        relation_type=rel.relation_type
    )
    db.add(db_rel)
    db.commit()
    db.refresh(db_rel)
    return db_rel

def get_relationship(db: Session, relationship_id: int):
    return db.query(models.Relationship).filter(models.Relationship.id == relationship_id).first()

def get_relationships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Relationship).offset(skip).limit(limit).all()

def update_relationship(db: Session, rel_db: models.Relationship, rel_data: schemas.RelationshipCreate):
    rel_db.source_term_id = rel_data.source_term_id
    rel_db.target_term_id = rel_data.target_term_id
    rel_db.relation_type = rel_data.relation_type
    db.commit()
    db.refresh(rel_db)
    return rel_db

def delete_relationship(db: Session, rel_db: models.Relationship):
    db.delete(rel_db)
    db.commit()

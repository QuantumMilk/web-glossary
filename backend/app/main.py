import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine
from .config import INIT_DB
from .models import Base


# Создаём таблицы (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Glossary API", description="CRUD + Semantic Graph for Microservices Terms")


# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    """
    Если установлена переменная окружения INIT_DB,
    то при старте произвести инициализацию БД данными из initial_data.json.
    """
    if INIT_DB:
        init_data()


@app.get("/")
def read_root():
    return {"message": "Hello from Glossary API on port 8080!"}


# -----------------------------------
# Вспомогательная функция инициализации
# -----------------------------------
def init_data():
    db = SessionLocal()
    try:
        # Очистим таблицы (для демонстрации, осторожно в реальных проектах!)
        db.query(models.Relationship).delete()
        db.query(models.Term).delete()
        db.commit()

        with open("data/initial_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1) Загружаем термины
        term_id_map = {}
        for idx, term_data in enumerate(data["terms"], start=1):
            term_create = schemas.TermCreate(**term_data)
            term_db = crud.create_term(db, term_create)
            term_id_map[idx] = term_db.id

        # 2) Загружаем связи
        for rel_data in data["relationships"]:
            # перепишем ID если нужно
            rel_data["source_term_id"] = term_id_map[rel_data["source_term_id"]]
            rel_data["target_term_id"] = term_id_map[rel_data["target_term_id"]]
            rel_create = schemas.RelationshipCreate(**rel_data)
            crud.create_relationship(db, rel_create)

        db.commit()
        print("Database initialized with initial_data.json")
    finally:
        db.close()


# -----------------------------------
# Создадим endpoint для принудительной инициализации (вручную)
# -----------------------------------
@app.post("/init-data", tags=["Initialization"])
def init_data_endpoint(db: Session = Depends(get_db)):
    """
    Удаляет все данные и загружает новые из initial_data.json
    """
    # Для большей безопасности это может быть защищено авторизацией.
    db.query(models.Relationship).delete()
    db.query(models.Term).delete()
    db.commit()

    with open("data/initial_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    term_id_map = {}
    for idx, term_data in enumerate(data["terms"], start=1):
        term_create = schemas.TermCreate(**term_data)
        term_db = crud.create_term(db, term_create)
        term_id_map[idx] = term_db.id

    for rel_data in data["relationships"]:
        rel_data["source_term_id"] = term_id_map[rel_data["source_term_id"]]
        rel_data["target_term_id"] = term_id_map[rel_data["target_term_id"]]
        rel_create = schemas.RelationshipCreate(**rel_data)
        crud.create_relationship(db, rel_create)

    return {"status": "Database re-initialized"}


# -----------------------------------
# Term CRUD endpoints
# -----------------------------------

@app.post("/terms", response_model=schemas.Term, tags=["Terms"])
def create_term_endpoint(term: schemas.TermCreate, db: Session = Depends(get_db)):
    db_term = crud.get_term_by_name(db, name=term.name)
    if db_term:
        raise HTTPException(status_code=400, detail="Term with this name already exists")
    return crud.create_term(db=db, term=term)


@app.get("/terms/{term_id}", response_model=schemas.Term, tags=["Terms"])
def read_term(term_id: int, db: Session = Depends(get_db)):
    db_term = crud.get_term(db, term_id=term_id)
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term


@app.get("/terms", response_model=list, tags=["Terms"])
def read_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terms = crud.get_terms(db, skip=skip, limit=limit)
    return terms


@app.put("/terms/{term_id}", response_model=schemas.Term, tags=["Terms"])
def update_term_endpoint(term_id: int, updates: schemas.TermUpdate, db: Session = Depends(get_db)):
    db_term = crud.get_term(db, term_id=term_id)
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return crud.update_term(db, db_term, updates)


@app.delete("/terms/{term_id}", tags=["Terms"])
def delete_term_endpoint(term_id: int, db: Session = Depends(get_db)):
    db_term = crud.get_term(db, term_id=term_id)
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    crud.delete_term(db, db_term)
    return {"detail": f"Term with id {term_id} deleted"}


# -----------------------------------
# Relationship CRUD endpoints
# -----------------------------------

@app.post("/relationships", response_model=schemas.Relationship, tags=["Relationships"])
def create_relationship_endpoint(rel: schemas.RelationshipCreate, db: Session = Depends(get_db)):
    # Проверяем, что source и target термины существуют
    source_term = crud.get_term(db, rel.source_term_id)
    target_term = crud.get_term(db, rel.target_term_id)
    if not source_term or not target_term:
        raise HTTPException(status_code=404, detail="Source or Target term not found")
    return crud.create_relationship(db, rel)


@app.get("/relationships/{relationship_id}", response_model=schemas.Relationship, tags=["Relationships"])
def read_relationship(relationship_id: int, db: Session = Depends(get_db)):
    relationship_db = crud.get_relationship(db, relationship_id)
    if not relationship_db:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return relationship_db


@app.get("/relationships", response_model=list, tags=["Relationships"])
def read_relationships(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_relationships(db, skip=skip, limit=limit)


@app.put("/relationships/{relationship_id}", response_model=schemas.Relationship, tags=["Relationships"])
def update_relationship_endpoint(relationship_id: int, rel_data: schemas.RelationshipCreate, db: Session = Depends(get_db)):
    relationship_db = crud.get_relationship(db, relationship_id)
    if not relationship_db:
        raise HTTPException(status_code=404, detail="Relationship not found")
    # Доп. проверка существования связанных терминов
    source_term = crud.get_term(db, rel_data.source_term_id)
    target_term = crud.get_term(db, rel_data.target_term_id)
    if not source_term or not target_term:
        raise HTTPException(status_code=404, detail="Source or Target term not found")

    return crud.update_relationship(db, relationship_db, rel_data)


@app.delete("/relationships/{relationship_id}", tags=["Relationships"])
def delete_relationship_endpoint(relationship_id: int, db: Session = Depends(get_db)):
    relationship_db = crud.get_relationship(db, relationship_id)
    if not relationship_db:
        raise HTTPException(status_code=404, detail="Relationship not found")
    crud.delete_relationship(db, relationship_db)
    return {"detail": f"Relationship with id {relationship_id} deleted"}

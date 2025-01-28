import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from .models import Base
from . import crud, schemas, models
from .config import INIT_DB

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Glossary API",
    description="CRUD + Semantic Graph for Microservices Terms",
)

# Разрешаем CORS, чтобы фронтенд на 3000 мог достучаться
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    if INIT_DB:
        init_data()

@app.get("/")
def root():
    return {"message": "Hello from Glossary API on port 8080!"}

# Функция инициализации (если INIT_DB=True или /init-data)
def init_data():
    db = SessionLocal()
    try:
        db.query(models.Relationship).delete()
        db.query(models.Term).delete()
        db.commit()

        with open("data/initial_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1) Термины
        term_id_map = {}
        for idx, term_data in enumerate(data["terms"], start=1):
            term_create = schemas.TermCreate(**term_data)
            term_db = crud.create_term(db, term_create)
            term_id_map[idx] = term_db.id

        # 2) Связи
        for rel_data in data["relationships"]:
            rel_data["source_term_id"] = term_id_map[rel_data["source_term_id"]]
            rel_data["target_term_id"] = term_id_map[rel_data["target_term_id"]]
            rel_create = schemas.RelationshipCreate(**rel_data)
            crud.create_relationship(db, rel_create)

        db.commit()
        print("Database initialized with data/initial_data.json")
    finally:
        db.close()

@app.post("/init-data")
def init_data_endpoint(db: Session = Depends(get_db)):
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

# ---------- CRUD для Term ----------
@app.post("/terms", response_model=schemas.Term)
def create_term_endpoint(term: schemas.TermCreate, db: Session = Depends(get_db)):
    existing = crud.get_term_by_name(db, term.name)
    if existing:
        raise HTTPException(status_code=400, detail="Term with this name already exists")
    return crud.create_term(db, term)

@app.get("/terms", response_model=list[schemas.Term])
def read_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_terms(db, skip, limit)

@app.get("/terms/{term_id}", response_model=schemas.Term)
def read_term(term_id: int, db: Session = Depends(get_db)):
    term = crud.get_term(db, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

@app.put("/terms/{term_id}", response_model=schemas.Term)
def update_term_endpoint(term_id: int, updates: schemas.TermUpdate, db: Session = Depends(get_db)):
    term_db = crud.get_term(db, term_id)
    if not term_db:
        raise HTTPException(status_code=404, detail="Term not found")
    return crud.update_term(db, term_db, updates)

@app.delete("/terms/{term_id}")
def delete_term_endpoint(term_id: int, db: Session = Depends(get_db)):
    term_db = crud.get_term(db, term_id)
    if not term_db:
        raise HTTPException(status_code=404, detail="Term not found")
    crud.delete_term(db, term_db)
    return {"detail": f"Term {term_id} deleted"}

# ---------- CRUD для Relationship ----------
@app.post("/relationships", response_model=schemas.Relationship)
def create_relationship_endpoint(rel: schemas.RelationshipCreate, db: Session = Depends(get_db)):
    source = crud.get_term(db, rel.source_term_id)
    target = crud.get_term(db, rel.target_term_id)
    if not source or not target:
        raise HTTPException(status_code=404, detail="Source or Target term not found")
    return crud.create_relationship(db, rel)

@app.get("/relationships", response_model=list[schemas.Relationship])
def read_relationships(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_relationships(db, skip, limit)

@app.get("/relationships/{relationship_id}", response_model=schemas.Relationship)
def read_relationship(relationship_id: int, db: Session = Depends(get_db)):
    relationship_db = crud.get_relationship(db, relationship_id)
    if not relationship_db:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return relationship_db

@app.put("/relationships/{relationship_id}", response_model=schemas.Relationship)
def update_relationship_endpoint(relationship_id: int, rel_data: schemas.RelationshipCreate, db: Session = Depends(get_db)):
    relationship_db = crud.get_relationship(db, relationship_id)
    if not relationship_db:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Дополнительно проверим, что термины есть
    source = crud.get_term(db, rel_data.source_term_id)
    target = crud.get_term(db, rel_data.target_term_id)
    if not source or not target:
        raise HTTPException(status_code=404, detail="Source or Target term not found")

    return crud.update_relationship(db, relationship_db, rel_data)

@app.delete("/relationships/{relationship_id}")
def delete_relationship_endpoint(relationship_id: int, db: Session = Depends(get_db)):
    relationship_db = crud.get_relationship(db, relationship_id)
    if not relationship_db:
        raise HTTPException(status_code=404, detail="Relationship not found")
    crud.delete_relationship(db, relationship_db)
    return {"detail": f"Relationship {relationship_id} deleted"}

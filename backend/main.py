from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import SessionLocal
from models import Detail, DetailUsageRule
from schemas import SuggestRequest
from logic import find_best_match

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------
# API 1: List Details
# ------------------------
@app.get("/details")
def list_details(db: Session = Depends(get_db)):
    return db.query(Detail).all()

# ------------------------
# API 2: Search
# ------------------------
@app.get("/details/search")
def search_details(q: str, db: Session = Depends(get_db)):
    results = db.query(Detail).filter(
        or_(
            Detail.title.ilike(f"%{q}%"),
            Detail.tags.ilike(f"%{q}%"),
            Detail.description.ilike(f"%{q}%")
        )
    ).all()
    return results

# ------------------------
# API 3: Suggest Detail
# ------------------------
@app.post("/suggest-detail")
def suggest_detail(request: SuggestRequest, db: Session = Depends(get_db)):
    rules = db.query(DetailUsageRule).all()

    best_rule, score = find_best_match(rules, request)

    if not best_rule or score == 0:
        return {"message": "No suitable detail found."}

    detail = db.query(Detail).filter(Detail.id == best_rule.detail_id).first()

    explanation = (
        f"Suggested because host_element='{best_rule.host_element}', "
        f"adjacent_element='{best_rule.adjacent_element}', "
        f"exposure='{best_rule.exposure}' matched."
    )

    return {
        "detail": {
            "id": detail.id,
            "title": detail.title,
            "description": detail.description
        },
        "explanation": explanation
    }
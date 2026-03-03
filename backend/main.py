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


# API 1: List Details

@app.get("/details")
def list_details(db: Session = Depends(get_db)):
    return db.query(Detail).all()


# API 2: Search

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


# API 3: Suggest Detail

@app.post("/suggest-detail")
def suggest_detail(request: SuggestRequest, db: Session = Depends(get_db)):

    # Fetching all usage rules
    rules = db.query(DetailUsageRule).all()

    # Run matching logic
    best_rule, score = find_best_match(rules, request)

    # Handle no match case
    if not best_rule or score == 0:
        return {"message": "No suitable detail found."}

    # Fetch associated detail
    detail = db.query(Detail).filter(
        Detail.id == best_rule.detail_id
    ).first()

    # Determine which fields matched (dynamic explanation)
    matched_fields = []

    if best_rule.host_element.lower() == request.host_element.lower():
        matched_fields.append("Host Element")

    if best_rule.adjacent_element.lower() == request.adjacent_element.lower():
        matched_fields.append("Adjacent Element")

    if best_rule.exposure.lower() == request.exposure.lower():
        matched_fields.append("Exposure")

    # Build explanation string
    if matched_fields:
        explanation = (
            "Suggested because the following context matched: "
            + ", ".join(matched_fields)
        )
    else:
        explanation = "Suggested based on closest available match."

    # Return structured response
    return {
        "detail": {
            "id": detail.id,
            "title": detail.title,
            "description": detail.description
        },
        "explanation": explanation,
        "match_score": score
    }

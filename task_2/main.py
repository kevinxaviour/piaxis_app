from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import SessionLocal
from models import User

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "role": u.role} for u in users]


@app.get("/secure/details")
def secure_details(x_user_email: str = Header(...), db: Session = Depends(get_db)):

    # find the user
    user = db.query(User).filter(User.email == x_user_email).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unknown email. Try: admin@piaxis.com | kevin@piaxis.com | naveen@piaxis.com"
        )

    # call the postgres function — filtering happens inside the DB
    # The function applies the exact same rules as the RLS policies
    rows = db.execute(
        text("SELECT * FROM get_details_for_user(:role, :uid)"),
        {"role": user.role, "uid": user.id}
    ).fetchall()

    result = [
        {
            "id":          r.id,
            "title":       r.title,
            "category":    r.category,
            "tags":        r.tags,
            "description": r.description,
            "source":      r.source,
            "owner_id":    r.owner_id,
        }
        for r in rows
    ]

    return {
        "authenticated_as": {"email": user.email, "role": user.role},
        "row_count": len(result),
        "details":   result
    }
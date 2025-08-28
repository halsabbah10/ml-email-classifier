from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import os

from database_sqlite import get_db, init_db, Email
from schemas import EmailCreate, EmailResponse
from classifier import EmailClassifier

app = FastAPI(title="Email Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = EmailClassifier()

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/api/emails", response_model=EmailResponse)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    category = classifier.classify(email.subject, email.body)
    
    db_email = Email(
        from_address=email.from_address,
        subject=email.subject,
        body=email.body,
        category=category,
        received_at=datetime.utcnow()
    )
    
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    
    return db_email

@app.get("/api/emails", response_model=List[EmailResponse])
def get_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emails = db.query(Email).order_by(Email.received_at.desc()).offset(skip).limit(limit).all()
    return emails

@app.get("/api/emails/{email_id}", response_model=EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8001))
    uvicorn.run("main_sqlite:app", host="0.0.0.0", port=port, reload=True)
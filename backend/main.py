from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from contextlib import asynccontextmanager
import os
import json

from database import get_db, init_db, Email
from schemas import EmailCreate, EmailResponse, EmailBatchUpload, BatchUploadResponse
from ml_classifier import MLEmailClassifier

classifier = MLEmailClassifier()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (cleanup code would go here if needed)

app = FastAPI(title="Email Classifier API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/api/emails/batch", response_model=BatchUploadResponse)
def batch_upload_emails(batch: EmailBatchUpload, db: Session = Depends(get_db)):
    success_count = 0
    failed_count = 0
    failed_emails = []
    
    for email_data in batch.emails:
        try:
            category = classifier.classify(email_data.subject, email_data.body)
            
            db_email = Email(
                from_address=email_data.from_address,
                subject=email_data.subject,
                body=email_data.body,
                category=category,
                received_at=datetime.utcnow()
            )
            
            db.add(db_email)
            db.commit()
            success_count += 1
        except Exception as e:
            failed_count += 1
            failed_emails.append({
                "email": email_data.dict(),
                "error": str(e)
            })
            db.rollback()
    
    return BatchUploadResponse(
        success_count=success_count,
        failed_count=failed_count,
        total_count=len(batch.emails),
        failed_emails=failed_emails,
        message=f"Processed {success_count} emails successfully, {failed_count} failed"
    )

@app.post("/api/emails/upload-json")
async def upload_json_files(files: List[UploadFile], db: Session = Depends(get_db)):
    
    total_success = 0
    total_failed = 0
    all_failed = []
    
    for file in files:
        if not file.filename.endswith('.json'):
            total_failed += 1
            all_failed.append({
                "file": file.filename,
                "error": "Not a JSON file"
            })
            continue
            
        try:
            content = await file.read()
            json_data = json.loads(content)
            
            # Handle both single email and array of emails
            emails_to_process = json_data if isinstance(json_data, list) else [json_data]
            
            batch = EmailBatchUpload(emails=[
                EmailCreate(
                    from_address=email.get('from_address', email.get('sender', email.get('from', 'unknown@email.com'))),
                    subject=email.get('subject', 'No Subject'),
                    body=email.get('body', email.get('content', email.get('message', '')))
                )
                for email in emails_to_process
            ])
            
            result = batch_upload_emails(batch, db)
            total_success += result.success_count
            total_failed += result.failed_count
            all_failed.extend(result.failed_emails)
            
        except Exception as e:
            total_failed += 1
            all_failed.append({
                "file": file.filename,
                "error": str(e)
            })
    
    return BatchUploadResponse(
        success_count=total_success,
        failed_count=total_failed,
        total_count=total_success + total_failed,
        failed_emails=all_failed,
        message=f"Processed {len(files)} files: {total_success} emails succeeded, {total_failed} failed"
    )

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
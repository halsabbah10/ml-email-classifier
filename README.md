# Email Classifier System

An automated email classification system that categorizes customer support emails into Billing Issue, Technical Support, Feedback, or Other categories.

## Features

- **Automatic Classification**: Uses keyword-based classification to categorize emails
- **Persistent Storage**: MySQL database for storing emails and their categories
- **REST API**: FastAPI backend for email ingestion and retrieval
- **Web Interface**: React TypeScript frontend to view and submit emails
- **Docker Support**: Easy deployment with Docker Compose

## Architecture

- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Frontend**: React with TypeScript
- **Database**: MySQL 8.0
- **Classification**: Rule-based classifier using keyword matching

## Prerequisites

- Docker and Docker Compose
- OR Node.js 18+, Python 3.11+, and MySQL 8.0

## Quick Start (Docker)

1. Clone the repository and navigate to the project directory:
```bash
cd "email classifier"
```

2. Start all services with Docker Compose:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Database Setup

1. Install MySQL 8.0
2. Create database:
```sql
CREATE DATABASE email_classifier;
```

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Update `.env` file with your MySQL credentials:
```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/email_classifier
API_PORT=8000
```

4. Run the backend:
```bash
python main.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the React app:
```bash
npm start
```

## Usage

### Submit an Email

1. Open the web interface at http://localhost:3000
2. Fill in the form:
   - **From Address**: Sender's email
   - **Subject**: Email subject
   - **Body**: Email content
3. Click "Submit Email"
4. The email will be automatically classified and stored

### View Emails

- All submitted emails appear in the "Recent Emails" section
- Each email shows:
  - Sender address
  - Subject and body preview
  - Assigned category (color-coded)
  - Submission timestamp

### API Endpoints

- `POST /api/emails` - Submit and classify a new email
- `GET /api/emails` - Retrieve all emails
- `GET /api/emails/{id}` - Get a specific email
- `GET /api/health` - Health check endpoint

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/emails" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "customer@example.com",
    "subject": "Cannot login to my account",
    "body": "I am getting an error when trying to login. The system says my password is incorrect but I know it is right."
  }'
```

## Classification Logic

The system uses keyword-based classification:

- **Billing Issue**: Keywords like "invoice", "payment", "refund", "subscription"
- **Technical Support**: Keywords like "error", "bug", "not working", "login"
- **Feedback**: Keywords like "suggestion", "recommend", "love", "review"
- **Other**: Emails that don't match other categories

## Testing the Pipeline

1. Submit a test email through the web interface
2. Verify it appears in the email list with correct category
3. Check the API response:
```bash
curl http://localhost:8000/api/emails
```

## Project Structure

```
email-classifier/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database models and connection
│   ├── classifier.py     # Email classification logic
│   ├── schemas.py        # Pydantic schemas
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx       # Main React component
│   │   ├── api.ts        # API client
│   │   ├── types.ts      # TypeScript types
│   │   └── App.css       # Styles
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Environment Variables

### Backend
- `DATABASE_URL`: MySQL connection string
- `API_PORT`: Backend server port (default: 8000)

### Frontend
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

## Troubleshooting

1. **Database connection error**: Ensure MySQL is running and credentials are correct
2. **Port already in use**: Change ports in docker-compose.yml or .env files
3. **Frontend can't reach backend**: Check CORS settings and API URL configuration

## Future Improvements

- Machine learning-based classification
- Email attachment handling
- User authentication
- Export functionality
- Advanced search and filtering
- Email analytics dashboard
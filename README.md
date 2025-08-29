# Email Classifier System

An advanced AI-powered email classification system that automatically categorizes customer support emails using machine learning. The system provides a modern web interface, REST API, and batch processing capabilities.

## 🚀 Features

- **Machine Learning Classification**: Uses scikit-learn with TF-IDF vectorization and Naive Bayes for 97%+ accuracy
- **Four Categories**: Automatically classifies emails as:
  - 📊 Billing Issue
  - 🔧 Technical Support
  - 💬 Feedback
  - 📝 Other
- **Multiple Input Methods**:
  - Manual email entry via web form
  - JSON file upload (single or batch)
  - REST API for programmatic access
- **Dual View Modes**: Toggle between card view and table view for email display
- **Real-time Processing**: Instant classification with confidence scores
- **Persistent Storage**: MySQL database with full data integrity
- **Modern UI**: Responsive design with animations and gradient themes

## 🏗️ Architecture

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React 18 with TypeScript
- **Database**: MySQL 8.0
- **ML Model**: Scikit-learn 1.7.0 (TF-IDF + Multinomial Naive Bayes)
- **Containerization**: Docker & Docker Compose support

## 📋 Prerequisites

### Option 1: Docker (Recommended)
- Docker Desktop 4.0+
- Docker Compose 2.0+
- 4GB RAM minimum
- 2GB disk space

### Option 2: Local Development
- Python 3.11 or 3.12
- Node.js 18+ and npm 9+
- MySQL 8.0
- 4GB RAM minimum

## 🚀 Quick Start

### Using Docker (Simplest - Everything Automated)

1. **Clone and navigate to the project:**
```bash
git clone https://github.com/halsabbah10/ml-email-classifier
cd "email classifier"
```

2. **Start all services:**
```bash
docker-compose up --build
```

3. **Access the application:**
- 🌐 **Web Interface**: http://localhost:3000
- 📡 **API Documentation**: http://localhost:8002/docs
- 🔌 **API Endpoint**: http://localhost:8002

That's it! The system will automatically:
- Create the MySQL database
- Train the ML model
- Start all services
- Be ready for use in ~2 minutes

### Manual Installation (For Development)

#### Step 1: Database Setup

1. **Install MySQL 8.0**

2. **Create database and user:**
```sql
CREATE DATABASE email_classifier;
CREATE USER 'email_user'@'127.0.0.1' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON email_classifier.* TO 'email_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```

#### Step 2: Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create Python virtual environment:**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Create `.env` file:**
```bash
cat > .env << 'EOF'
DATABASE_URL=mysql+pymysql://email_user:your_password@127.0.0.1:3306/email_classifier
API_PORT=8002
EOF
```

5. **Start the backend:**
```bash
python main.py
```

The backend will:
- Connect to MySQL
- Create tables automatically
- Train the ML model (first run only)
- Start serving on http://localhost:8002

#### Step 3: Frontend Setup

1. **Open new terminal and navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm start
```

4. **Access the application:**
- Open http://localhost:3000 in your browser

## 📘 Usage Guide

### Web Interface

#### Manual Email Submission
1. Click "✍️ Manual Entry" tab
2. Fill in:
   - **From Address**: Sender's email
   - **Subject**: Email subject line
   - **Body**: Email content
3. Click "Submit Email"
4. View instant classification result

#### JSON File Upload
1. Click "📁 JSON Upload" tab
2. Prepare JSON file in this format:
```json
[
  {
    "from_address": "customer@example.com",
    "subject": "Billing inquiry",
    "body": "I have a question about my invoice..."
  },
  {
    "from_address": "user@example.com",
    "subject": "App not working",
    "body": "The application crashes when I try to login..."
  }
]
```
3. Drag & drop or click to select files
4. Click "Upload & Classify"
5. View batch processing results

#### Viewing Emails
- **Card View** (default): Detailed view with full email content
- **Table View**: Compact tabular format for scanning many emails
- Toggle between views using the view switcher

### API Usage

#### Submit Single Email
```bash
curl -X POST "http://localhost:8002/api/emails" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "customer@example.com",
    "subject": "Cannot access my account",
    "body": "I keep getting an error when trying to login. Please help!"
  }'
```

Response:
```json
{
  "id": 1,
  "from_address": "customer@example.com",
  "subject": "Cannot access my account",
  "body": "I keep getting an error when trying to login. Please help!",
  "category": "Technical Support",
  "received_at": "2025-08-28T19:30:00"
}
```

#### Upload JSON Files
```bash
curl -X POST "http://localhost:8002/api/emails/upload-json" \
  -F "files=@emails.json"
```

#### Retrieve All Emails
```bash
curl -X GET "http://localhost:8002/api/emails"
```

#### Get Specific Email
```bash
curl -X GET "http://localhost:8002/api/emails/1"
```

### Testing the System

Run the comprehensive test suite:
```bash
cd backend
python test_email.py
```

This will:
- Test all API endpoints
- Submit sample emails
- Test JSON file upload
- Verify classification accuracy
- Display results summary

## 🧠 Machine Learning Model

### Training Data
- **CSV Dataset**: 240 real-world customer emails
- **Synthetic Data**: 36 additional examples for edge cases
- **Total**: 276 training examples

### Model Performance
- **Algorithm**: TF-IDF Vectorization + Multinomial Naive Bayes
- **Accuracy**: 97.1% on test set
- **Features**: Trigrams, stop word removal, optimized parameters
- **Training Time**: < 1 second
- **Prediction Time**: < 50ms per email

### Classification Categories

| Category | Keywords/Patterns | Confidence |
|----------|------------------|------------|
| Billing Issue | invoice, payment, charge, refund, subscription | 99.8%+ |
| Technical Support | error, bug, crash, login, not working | 88.0%+ |
| Feedback | great, love, suggestion, improve, recommendation | 97.9%+ |
| Other | partnership, inquiry, general questions | 99.0%+ |

## 📁 Project Structure

```
email-classifier/
├── backend/
│   ├── main.py              # FastAPI application with lifespan management
│   ├── database.py          # SQLAlchemy models and MySQL connection
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── ml_classifier.py     # Machine learning classification engine
│   ├── test_email.py        # Comprehensive test suite
│   ├── requirements.txt     # Python dependencies (updated)
│   ├── .env                 # Environment variables (create this)
│   ├── email_classifier_model.joblib  # Trained ML model (auto-generated)
│   ├── venv/               # Python virtual environment
│   └── Dockerfile          # Container configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component with dual views
│   │   ├── App.css         # Modern styling with animations
│   │   ├── api.ts          # Axios API client
│   │   ├── types.ts        # TypeScript interfaces
│   │   └── index.tsx       # Application entry point
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── package.json        # Node dependencies
│   ├── tsconfig.json       # TypeScript configuration
│   └── Dockerfile          # Container configuration
│
├── data/
│   └── emails_dataset.csv  # Training data for ML model
│
├── .vscode/
│   └── settings.json       # IDE configuration for Python environment
│
├── docker-compose.yml      # Multi-container orchestration
├── pyrightconfig.json      # Pylance/Pyright configuration
├── README.md              # This file
└── .env.example           # Environment variables template
```

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/email_classifier

# API Configuration
API_PORT=8002
```

#### Frontend
The frontend automatically connects to the backend at http://localhost:8002.
To change this, modify `src/api.ts`:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';
```

### Docker Configuration

#### Ports
- Frontend: 3000
- Backend: 8002
- MySQL: 3306

To change ports, modify `docker-compose.yml`.

## 🐛 Troubleshooting

### Common Issues

#### MySQL Connection Failed
```
Error: Access denied for user 'root'@'localhost'
```
**Solution**: Use IP address instead of localhost:
```bash
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/email_classifier
```

#### Port Already in Use
```
Error: Address already in use
```
**Solution**: Find and kill the process:
```bash
lsof -ti:8002 | xargs kill -9  # For backend
lsof -ti:3000 | xargs kill -9  # For frontend
```

#### Scikit-learn Version Warning
```
InconsistentVersionWarning: Trying to unpickle estimator
```
**Solution**: Delete and retrain the model:
```bash
cd backend
rm email_classifier_model.joblib
python -c "from ml_classifier import MLEmailClassifier; MLEmailClassifier()"
```

#### Frontend Can't Connect to Backend
**Solution**: Ensure backend is running on port 8002 and check CORS settings.

#### IDE Import Errors (Pylance)
**Solution**: Select the correct Python interpreter:
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
2. Type "Python: Select Interpreter"
3. Choose `./backend/venv/bin/python`

## 🧪 Testing

### Unit Tests
```bash
cd backend
python test_email.py
```

### Manual Testing Checklist
- [ ] Submit email via web form
- [ ] Upload single JSON file
- [ ] Upload multiple JSON files
- [ ] Toggle between card and table views
- [ ] Check all 4 classification categories
- [ ] Verify API endpoints via curl
- [ ] Test database persistence

## 🚢 Deployment

### Production with Docker

1. **Update environment variables for production:**
```yaml
# docker-compose.prod.yml
environment:
  - DATABASE_URL=mysql+pymysql://prod_user:strong_password@mysql:3306/email_classifier
  - API_PORT=8002
  - REACT_APP_API_URL=https://api.yourdomain.com
```

2. **Build and run:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Set up reverse proxy (nginx example):**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3000;
    }
    
    location /api {
        proxy_pass http://localhost:8002;
    }
}
```

## 📊 Performance Metrics

- **API Response Time**: < 100ms average
- **Classification Speed**: < 50ms per email
- **Batch Processing**: 100+ emails/second
- **Model Accuracy**: 97.1%
- **Frontend Load Time**: < 2 seconds
- **Memory Usage**: < 500MB (backend), < 200MB (frontend)

## 🔒 Security Considerations

1. **Database**: Use strong passwords, restrict user privileges
2. **API**: Implement rate limiting for production
3. **Frontend**: Sanitize all user inputs
4. **Docker**: Use specific version tags, not `latest`
5. **Secrets**: Never commit `.env` files

## 📝 Future Enhancements

- [ ] User authentication and authorization
- [ ] Email attachment processing
- [ ] Advanced search and filtering
- [ ] Export functionality (CSV, PDF)
- [ ] Real-time notifications
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Deep learning models for better accuracy
- [ ] Email template responses
- [ ] Webhook integrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review closed issues on GitHub
3. Open a new issue with:
   - System information
   - Error messages
   - Steps to reproduce

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the frontend library
- Scikit-learn for ML capabilities
- MySQL for reliable data storage

---
Built with ❤️ for efficient email management
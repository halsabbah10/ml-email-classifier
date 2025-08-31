import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from database import CategoryEnum

class MLEmailClassifier:
    def __init__(self):
        """Initialize the email classifier with pre-trained model"""
        self.model_path = 'email_classifier.pkl'
        self.pipeline = None
        self.load_model()

    def load_model(self):
        """Load the pre-trained model"""
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            raise FileNotFoundError(f"Model file {self.model_path} not found.")
    
    def classify(self, subject: str, body: str) -> CategoryEnum:
        """Classify an email using the ML model"""
        if self.pipeline is None:
            raise RuntimeError("Model not loaded.")
        
        # Combine subject and body
        text = f"{subject} {body}"
        
        # Predict using the model
        prediction = self.pipeline.predict([text])[0]
        
        # Convert string prediction to CategoryEnum
        category_mapping = {
            "Billing Issue": CategoryEnum.BILLING,
            "Technical Support": CategoryEnum.TECHNICAL,
            "Feedback": CategoryEnum.FEEDBACK,
            "Other": CategoryEnum.OTHER
        }
        
        return category_mapping.get(prediction, CategoryEnum.OTHER)
    
    def get_prediction_confidence(self, subject: str, body: str):
        """Get prediction with confidence scores"""
        if self.pipeline is None:
            return None
        
        text = f"{subject} {body}"
        prediction = self.pipeline.predict([text])[0]
        
        # Try to get probability scores if available
        try:
            probabilities = self.pipeline.predict_proba([text])[0]
            classes = self.pipeline.classes_
            confidence_scores = dict(zip(classes, probabilities))
            confidence = max(probabilities)
        except AttributeError:
            # For LinearSVC without probability support
            confidence_scores = {prediction: 1.0}
            confidence = 1.0
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'all_scores': confidence_scores
        }

    @staticmethod
    def create_model_pipeline():
        """Create the exact pipeline used by the current model (for reference/training)"""
        return Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,          # Match current model
                ngram_range=(1, 2),         # Match current model
                min_df=2,
                max_df=0.95,
                stop_words='english',
                sublinear_tf=False,         # Match current model exactly
                use_idf=True
            )),
            ('clf', LinearSVC(              # Match current model
                C=1.0,                      # Match current model
                random_state=42,
                max_iter=3000,              # Match current model exactly
                class_weight='balanced'     # Match current model
            ))
        ])

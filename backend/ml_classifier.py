import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from database import CategoryEnum

class MLEmailClassifier:
    def __init__(self):
        # Define model path
        self.model_path = 'email_classifier.pkl'
        self.pipeline = None
        self.load_or_train_model()
    
    def load_csv_data(self):
        """Load user's CSV dataset"""
        csv_path = '../data/emails_dataset.csv'
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Map CSV columns to our format
            df = df.rename(columns={'label': 'category'})
            return df[['subject', 'body', 'category']]
        return pd.DataFrame(columns=['subject', 'body', 'category'])

    def get_additional_training_data(self):
        """Generate additional diverse training examples"""
        additional_data = [
            # More Billing Issues
            ("Double charged this month", "I was charged twice for my subscription this month, please refund one", "Billing Issue"),
            ("Promo code expired", "The discount code I received via email is showing as expired", "Billing Issue"),
            ("Upgrade billing question", "How much will it cost to upgrade to the premium plan?", "Billing Issue"),
            ("Tax invoice needed", "Can you please provide a tax-compliant invoice for accounting?", "Billing Issue"),
            ("Payment method declined", "My payment was declined but my card is valid", "Billing Issue"),
            ("Subscription not cancelled", "I cancelled last month but was still charged", "Billing Issue"),
            ("Free trial extended", "Can you extend my free trial by a few more days?", "Billing Issue"),
            ("Corporate billing setup", "How do I set up corporate billing for our team?", "Billing Issue"),
            
            # More Technical Support  
            ("Mobile app crashes", "The mobile app crashes every time I try to sync", "Technical Support"),
            ("Data not syncing", "My data isn't syncing between desktop and mobile versions", "Technical Support"),
            ("Two-factor auth issues", "Can't receive 2FA codes on my phone", "Technical Support"),
            ("Browser compatibility", "The website doesn't work properly in Safari", "Technical Support"),
            ("Import file corrupted", "When I try to import my CSV file it says it's corrupted", "Technical Support"),
            ("Dashboard loading slow", "The dashboard takes forever to load my data", "Technical Support"),
            ("Email notifications stopped", "I'm not receiving email notifications anymore", "Technical Support"),
            ("Search not working", "The search function returns no results even for exact matches", "Technical Support"),
            
            # More Feedback
            ("Loving the new features", "The recent updates are fantastic, especially the dark mode", "Feedback"),
            ("Could use better mobile app", "The mobile experience could be improved significantly", "Feedback"),
            ("Customer support is amazing", "Your support team resolved my issue in minutes!", "Feedback"),
            ("Interface too complicated", "The new interface is confusing and hard to navigate", "Feedback"),
            ("Missing key feature", "Would be perfect if you added integration with Slack", "Feedback"),
            ("Performance improvements needed", "The app has been getting slower with recent updates", "Feedback"),
            ("Great value for money", "Best tool in this price range, very satisfied", "Feedback"),
            ("Documentation needs work", "The help documentation is outdated and confusing", "Feedback"),
            
            # More Other/Business
            ("Media interview request", "We're writing an article about customer service tools", "Other"),
            ("Academic research study", "PhD student studying SaaS adoption patterns", "Other"),
            ("Conference speaking opportunity", "Would you like to speak at our upcoming tech conference?", "Other"),
            ("Vendor partnership inquiry", "We provide payment processing services for SaaS companies", "Other"),
            ("Legal compliance question", "Need to understand your data retention policies", "Other"),
            ("Enterprise sales inquiry", "Interested in enterprise pricing for 500+ users", "Other"),
            ("Integration partnership", "We'd like to build an integration with your API", "Other"),
            ("Charity discount request", "We're a registered charity, do you offer discounts?", "Other"),
            ("Job opportunity", "Are you hiring remote developers?", "Other"),
            ("Office visit request", "Can we schedule a tour of your offices?", "Other"),
            ("Competitor analysis", "Market research about customer service software", "Other"),
            ("Investment inquiry", "Venture capital firm interested in learning more", "Other"),
        ]
        return pd.DataFrame(additional_data, columns=['subject', 'body', 'category'])

    def get_training_data(self):
        """Combine CSV data with additional training examples"""
        # Load CSV data
        csv_data = self.load_csv_data()
        print(f"Loaded {len(csv_data)} examples from CSV")
        
        # Get additional examples
        additional_data = self.get_additional_training_data()
        print(f"Added {len(additional_data)} additional examples")
        
        # Combine both datasets
        if len(csv_data) > 0:
            combined_data = pd.concat([csv_data, additional_data], ignore_index=True)
        else:
            combined_data = additional_data
        
        print(f"Total training examples: {len(combined_data)}")
        return combined_data
    
    def train_model(self):
        """Train the ML model"""
        print("Training ML classifier...")
        
        # Get training data
        df = self.get_training_data()
        
        # Combine subject and body
        df['text'] = df['subject'] + ' ' + df['body']
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                stop_words='english', 
                ngram_range=(1, 3),  # Include trigrams
                max_features=2000,   # More features for larger dataset
                min_df=2,           # Ignore terms that appear in less than 2 documents
                max_df=0.95         # Ignore terms that appear in more than 95% of documents
            )),
            ('classifier', MultinomialNB(alpha=0.01))  # Lower alpha for better performance
        ])
        
        # Split data with larger test size for more reliable evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            df['text'], df['category'], test_size=0.25, random_state=42, stratify=df['category']
        )
        
        # Train the model
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save the model
        joblib.dump(self.pipeline, self.model_path)
        print(f"Model saved to {self.model_path}")
    
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        if os.path.exists(self.model_path):
            print("Loading ML model...")
            self.pipeline = joblib.load(self.model_path)
        else:
            print("No existing model found. Training new model...")
            self.train_model()
    
    def classify(self, subject: str, body: str) -> CategoryEnum:
        """Classify an email using the ML model"""
        if self.pipeline is None:
            # Fallback to training if model not loaded
            self.train_model()
        
        # Combine subject and body
        text = f"{subject} {body}"
        
        # Predict
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
        
        # Some models don't have predict_proba (like LinearSVC)
        try:
            probabilities = self.pipeline.predict_proba([text])[0]
            classes = self.pipeline.classes_
            confidence_scores = dict(zip(classes, probabilities))
            confidence = max(probabilities)
        except AttributeError:
            # For models without probability support
            confidence_scores = {prediction: 1.0}
            confidence = 1.0
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'all_scores': confidence_scores
        }
import re
from database import CategoryEnum

class EmailClassifier:
    def __init__(self):
        self.billing_keywords = [
            'invoice', 'payment', 'billing', 'charge', 'refund', 'subscription',
            'bill', 'receipt', 'transaction', 'credit card', 'debit', 'overdue',
            'fee', 'cost', 'price', 'discount', 'promo code', 'coupon'
        ]
        
        self.technical_keywords = [
            'error', 'bug', 'crash', 'not working', 'broken', 'issue', 'problem',
            'cannot', 'unable', 'failed', 'failure', 'timeout', 'slow', 'performance',
            'login', 'password', 'access', 'permission', 'install', 'update',
            'download', 'upload', 'connection', '404', '500', 'server'
        ]
        
        self.feedback_keywords = [
            'feedback', 'suggestion', 'recommend', 'improve', 'love', 'great',
            'excellent', 'good', 'bad', 'terrible', 'review', 'rating', 'opinion',
            'think', 'feel', 'wish', 'would like', 'feature request', 'idea'
        ]
    
    def classify(self, subject: str, body: str) -> CategoryEnum:
        text = (subject + " " + body).lower()
        
        billing_score = sum(1 for keyword in self.billing_keywords if keyword in text)
        technical_score = sum(1 for keyword in self.technical_keywords if keyword in text)
        feedback_score = sum(1 for keyword in self.feedback_keywords if keyword in text)
        
        billing_score = billing_score * 1.5 if any(word in subject.lower() for word in ['bill', 'invoice', 'payment']) else billing_score
        technical_score = technical_score * 1.5 if any(word in subject.lower() for word in ['error', 'bug', 'not working']) else technical_score
        
        scores = {
            CategoryEnum.BILLING: billing_score,
            CategoryEnum.TECHNICAL: technical_score,
            CategoryEnum.FEEDBACK: feedback_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            return CategoryEnum.OTHER
        
        for category, score in scores.items():
            if score == max_score:
                return category
        
        return CategoryEnum.OTHER
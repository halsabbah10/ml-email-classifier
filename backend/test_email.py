#!/usr/bin/env python3
import requests
import json
import time

API_URL = "http://localhost:8000"

test_emails = [
    {
        "from_address": "john.doe@example.com",
        "subject": "Invoice Payment Issue",
        "body": "I tried to pay my invoice #12345 but my credit card was declined. Can you help me resolve this billing issue?"
    },
    {
        "from_address": "jane.smith@company.com",
        "subject": "Login Error - Cannot Access Account",
        "body": "I'm getting an error message when trying to login. It says 'Invalid credentials' but I'm sure my password is correct. This bug is preventing me from accessing my account."
    },
    {
        "from_address": "feedback@customer.org",
        "subject": "Great Service!",
        "body": "I just wanted to say that your product is excellent! I love the new features and would recommend it to others. Keep up the good work!"
    },
    {
        "from_address": "support@business.net",
        "subject": "General Inquiry",
        "body": "Hello, I wanted to know more about your services and pricing plans. Please send me more information."
    },
    {
        "from_address": "alice@startup.io",
        "subject": "Refund Request",
        "body": "I was charged twice for my subscription this month. Please process a refund for the duplicate charge."
    }
]

def test_api():
    print("Testing Email Classifier API...")
    print("-" * 50)
    
    # Health check
    try:
        response = requests.get(f"{API_URL}/api/health")
        if response.status_code == 200:
            print("✓ API is healthy")
        else:
            print("✗ API health check failed")
            return
    except Exception as e:
        print(f"✗ Cannot connect to API: {e}")
        print("Make sure the backend is running on port 8000")
        return
    
    # Submit test emails
    print("\nSubmitting test emails...")
    for email in test_emails:
        try:
            response = requests.post(
                f"{API_URL}/api/emails",
                json=email,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Email from {email['from_address'][:20]:20} → Category: {result['category']}")
            else:
                print(f"✗ Failed to submit email from {email['from_address']}")
        except Exception as e:
            print(f"✗ Error submitting email: {e}")
        
        time.sleep(0.5)
    
    # Retrieve emails
    print("\nRetrieving all emails...")
    try:
        response = requests.get(f"{API_URL}/api/emails")
        if response.status_code == 200:
            emails = response.json()
            print(f"✓ Retrieved {len(emails)} emails from database")
            
            # Show category distribution
            categories = {}
            for email in emails:
                cat = email['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            print("\nCategory Distribution:")
            for cat, count in categories.items():
                print(f"  - {cat}: {count}")
        else:
            print("✗ Failed to retrieve emails")
    except Exception as e:
        print(f"✗ Error retrieving emails: {e}")
    
    print("\n" + "-" * 50)
    print("Testing complete! Check http://localhost:3000 to view the emails in the web interface.")

if __name__ == "__main__":
    test_api()
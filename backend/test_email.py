#!/usr/bin/env python3
import requests
import json
import time
import tempfile
import os

API_URL = "http://localhost:8002"

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
        print("Make sure the backend is running on port 8002")
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

def test_json_upload():
    print("\nTesting JSON File Upload...")
    print("-" * 30)
    
    # Create test JSON files
    test_json_data1 = [
        {
            "from_address": "upload_test1@example.com",
            "subject": "Billing inquiry via upload",
            "body": "I have a question about my invoice charges. Please help me understand the billing details."
        },
        {
            "from_address": "upload_test2@example.com", 
            "subject": "Technical issue via upload",
            "body": "The application is crashing when I try to save my work. This is a critical bug."
        }
    ]
    
    test_json_data2 = {
        "from_address": "upload_test3@example.com",
        "subject": "Great feedback via upload", 
        "body": "I love the new features you've added! The user interface is much better now."
    }
    
    try:
        # Create temporary JSON files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
            json.dump(test_json_data1, f1)
            file1_path = f1.name
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
            json.dump(test_json_data2, f2)
            file2_path = f2.name
        
        print(f"Created test files: {os.path.basename(file1_path)}, {os.path.basename(file2_path)}")
        
        # Test single file upload
        print("\nTesting single file upload...")
        with open(file1_path, 'rb') as f:
            files = {'files': f}
            response = requests.post(f"{API_URL}/api/emails/upload-json", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Single file upload successful: {result['success_count']} emails processed")
        else:
            print(f"✗ Single file upload failed: {response.status_code}")
        
        # Test multiple file upload
        print("\nTesting multiple file upload...")
        with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
            files = [
                ('files', f1),
                ('files', f2)
            ]
            response = requests.post(f"{API_URL}/api/emails/upload-json", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Multiple file upload successful: {result['success_count']} emails, {result['failed_count']} failed")
            print(f"  Message: {result['message']}")
        else:
            print(f"✗ Multiple file upload failed: {response.status_code}")
            
    except Exception as e:
        print(f"✗ JSON upload test error: {e}")
    finally:
        # Clean up temporary files
        try:
            os.unlink(file1_path)
            os.unlink(file2_path)
        except (OSError, FileNotFoundError):
            pass

if __name__ == "__main__":
    test_api()
    test_json_upload()
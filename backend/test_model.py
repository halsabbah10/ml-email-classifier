import json
from ml_classifier import MLEmailClassifier

# Test the model with previously problematic examples
print("Testing ML Model")
print("=" * 50)

classifier = MLEmailClassifier()

# Load the test examples from the JSON file
with open('../test_feedback_issues.json', 'r') as f:
    test_emails = json.load(f)

# Add more test cases
additional_tests = [
    {
        "from_address": "sarah@company.com",
        "subject": "Feature request for workflow automation", 
        "body": "Would love automation feature to streamline our approval workflow"
    },
    {
        "from_address": "mike@startup.io",
        "subject": "UI improvement suggestion",
        "body": "The navigation menu would be better if it was collapsible"
    },
    {
        "from_address": "alex@tech.co",
        "subject": "Performance optimization feedback",
        "body": "The dashboard loads slowly with large datasets. Consider implementing pagination or lazy loading to improve user experience."
    }
]

all_tests = test_emails + additional_tests

print("Testing feedback classification accuracy:")
print("=" * 50)

correct_predictions = 0
total_predictions = len(all_tests)

for i, email in enumerate(all_tests, 1):
    prediction = classifier.classify(email['subject'], email['body'])
    confidence_info = classifier.get_prediction_confidence(email['subject'], email['body'])
    
    is_correct = prediction.value == 'Feedback'
    if is_correct:
        correct_predictions += 1
        status = "✓ CORRECT"
    else:
        status = "✗ INCORRECT"
    
    print(f"\n{i}. Subject: {email['subject']}")
    print(f"   Predicted: {prediction.value}")
    print(f"   Expected: Feedback")
    print(f"   Status: {status}")
    if confidence_info:
        print(f"   Confidence: {confidence_info['confidence']:.3f}")

print("\n" + "=" * 50)
print(f"RESULTS: {correct_predictions}/{total_predictions} correct")
print(f"Accuracy: {(correct_predictions/total_predictions)*100:.1f}%")

# Test some non-feedback examples to ensure they're still classified correctly
print("\n" + "=" * 50)
print("Testing non-feedback examples:")
print("=" * 50)

non_feedback_tests = [
    {
        "subject": "Double charged this month",
        "body": "I was charged twice for my subscription, please refund",
        "expected": "Billing Issue"
    },
    {
        "subject": "App crashes on login",
        "body": "The mobile app crashes every time I try to log in",
        "expected": "Technical Support"
    },
    {
        "subject": "Partnership inquiry",
        "body": "We're interested in becoming a reseller of your product",
        "expected": "Other"
    }
]

for i, email in enumerate(non_feedback_tests, 1):
    prediction = classifier.classify(email['subject'], email['body'])
    confidence_info = classifier.get_prediction_confidence(email['subject'], email['body'])
    
    is_correct = prediction.value == email['expected']
    status = "✓ CORRECT" if is_correct else "✗ INCORRECT"
    
    print(f"\n{i}. Subject: {email['subject']}")
    print(f"   Predicted: {prediction.value}")
    print(f"   Expected: {email['expected']}")
    print(f"   Status: {status}")
    if confidence_info:
        print(f"   Confidence: {confidence_info['confidence']:.3f}")

print("\n" + "=" * 50)
print("🎉 Model testing complete!")
print("The model should now correctly classify feedback emails.")
print("=" * 50)
import React, { useState, useEffect } from 'react';
import './App.css';
import { Email, EmailCreate } from './types';
import { emailApi } from './api';

function App() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState<EmailCreate>({
    from_address: '',
    subject: '',
    body: ''
  });

  useEffect(() => {
    loadEmails();
  }, []);

  const loadEmails = async () => {
    try {
      setLoading(true);
      const data = await emailApi.getEmails();
      setEmails(data);
    } catch (err) {
      setError('Failed to load emails');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await emailApi.createEmail(formData);
      setSuccess(true);
      setFormData({ from_address: '', subject: '', body: '' });
      await loadEmails();
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError('Failed to submit email');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const getCategoryClass = (category: string) => {
    switch (category) {
      case 'Billing Issue':
        return 'category-billing';
      case 'Technical Support':
        return 'category-technical';
      case 'Feedback':
        return 'category-feedback';
      default:
        return 'category-other';
    }
  };

  const formatDate = (dateString: string) => {
    // Create date from UTC string and convert to local time
    const date = new Date(dateString + 'Z'); // Add 'Z' to indicate UTC if not present
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
      timeZoneName: 'short'
    });
  };

  return (
    <div className="app">
      <div className="header">
        <h1>Email Classifier System</h1>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="container">
        <div className="form-section">
          <h2>Submit New Email</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="from_address">From Address:</label>
              <input
                type="email"
                id="from_address"
                name="from_address"
                value={formData.from_address}
                onChange={handleInputChange}
                required
                placeholder="sender@example.com"
              />
            </div>
            <div className="form-group">
              <label htmlFor="subject">Subject:</label>
              <input
                type="text"
                id="subject"
                name="subject"
                value={formData.subject}
                onChange={handleInputChange}
                required
                placeholder="Email subject..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="body">Body:</label>
              <textarea
                id="body"
                name="body"
                value={formData.body}
                onChange={handleInputChange}
                required
                placeholder="Email content..."
              />
            </div>
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit Email'}
            </button>
            {success && <div className="success-message">Email submitted and classified successfully!</div>}
          </form>
        </div>

        <div className="emails-section">
          <h2>Recent Emails</h2>
          {loading && <div className="loading">Loading emails...</div>}
          <div className="email-list">
            {emails.map((email) => (
              <div key={email.id} className="email-item">
                <div className="email-header">
                  <div className="email-from">{email.from_address}</div>
                  <span className={`email-category ${getCategoryClass(email.category)}`}>
                    {email.category}
                  </span>
                </div>
                <div className="email-subject">{email.subject}</div>
                <div className="email-body">{email.body}</div>
                <div className="email-date">{formatDate(email.received_at)}</div>
              </div>
            ))}
            {emails.length === 0 && !loading && (
              <div className="loading">No emails yet. Submit your first email!</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
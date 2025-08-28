import React, { useState, useEffect } from 'react';
import './App.css';
import { Email, EmailCreate } from './types';
import { emailApi } from './api';

function App() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [uploadMode, setUploadMode] = useState<'file' | 'manual'>('file');
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);
  const [uploadProgress, setUploadProgress] = useState<string>('');
  const [viewMode, setViewMode] = useState<'cards' | 'table'>('cards');
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
    if (uploadMode === 'file') {
      await handleFileUpload();
    } else {
      await handleManualSubmit();
    }
  };

  const handleManualSubmit = async () => {
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

  const handleFileUpload = async () => {
    if (!selectedFiles || selectedFiles.length === 0) {
      setError('Please select at least one JSON file');
      return;
    }

    setLoading(true);
    setUploadProgress('Uploading files to server...');

    try {
      const result = await emailApi.uploadJsonFiles(selectedFiles);
      
      setUploadProgress(result.message);
      setSuccess(true);
      
      if (result.failed_count > 0) {
        console.warn('Some emails failed to process:', result.failed_emails);
        setError(`${result.failed_count} emails failed to process. Check console for details.`);
      }
      
      await loadEmails();
      setTimeout(() => {
        setSuccess(false);
        setUploadProgress('');
        setSelectedFiles(null);
        if (result.failed_count === 0) {
          setError(null);
        }
      }, 4000);
    } catch (err) {
      setError(`Upload failed: ${err}`);
      console.error('Upload error:', err);
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
          <h2>Submit Emails</h2>
          
          <div className="upload-mode-toggle">
            <button 
              className={`mode-btn ${uploadMode === 'file' ? 'active' : ''}`}
              onClick={() => setUploadMode('file')}
              type="button"
            >
              📁 JSON Upload
            </button>
            <button 
              className={`mode-btn ${uploadMode === 'manual' ? 'active' : ''}`}
              onClick={() => setUploadMode('manual')}
              type="button"
            >
              ✍️ Manual Entry
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {uploadMode === 'file' ? (
              <div className="file-upload-section">
                <div className="form-group">
                  <label htmlFor="file-upload" className="file-upload-label">
                    <div className="file-upload-box">
                      <div className="upload-icon">📤</div>
                      <div className="upload-text">
                        {selectedFiles && selectedFiles.length > 0 
                          ? `${selectedFiles.length} file(s) selected`
                          : 'Click to select JSON files or drag & drop'
                        }
                      </div>
                      <div className="upload-hint">Supports single or batch uploads</div>
                    </div>
                  </label>
                  <input
                    type="file"
                    id="file-upload"
                    accept=".json,application/json"
                    multiple
                    onChange={(e) => setSelectedFiles(e.target.files)}
                    style={{ display: 'none' }}
                  />
                </div>
                {selectedFiles && selectedFiles.length > 0 && (
                  <div className="selected-files">
                    {Array.from(selectedFiles).map((file, idx) => (
                      <div key={idx} className="file-item">
                        📄 {file.name} ({(file.size / 1024).toFixed(2)} KB)
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <>
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
              </>
            )}
            
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Processing...' : uploadMode === 'file' ? 'Upload & Classify' : 'Submit Email'}
            </button>
            
            {uploadProgress && <div className="upload-progress">{uploadProgress}</div>}
            {success && <div className="success-message">
              {uploadMode === 'file' ? uploadProgress : 'Email submitted and classified successfully!'}
            </div>}
          </form>
        </div>

        <div className="emails-section">
          <div className="emails-header">
            <h2>Recent Emails</h2>
            <div className="view-toggle">
              <button 
                className={`view-btn ${viewMode === 'cards' ? 'active' : ''}`}
                onClick={() => setViewMode('cards')}
                type="button"
              >
                📋 Cards
              </button>
              <button 
                className={`view-btn ${viewMode === 'table' ? 'active' : ''}`}
                onClick={() => setViewMode('table')}
                type="button"
              >
                📊 Table
              </button>
            </div>
          </div>
          {loading && <div className="loading">Loading emails...</div>}
          {viewMode === 'table' ? (
            <div className="table-view">
              <table className="emails-table">
                <thead>
                  <tr>
                    <th>From</th>
                    <th>Subject</th>
                    <th>Category</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {emails.map((email) => (
                    <tr key={email.id}>
                      <td className="email-from-cell">{email.from_address}</td>
                      <td className="email-subject-cell" title={email.subject}>
                        {email.subject.length > 50 ? email.subject.substring(0, 50) + '...' : email.subject}
                      </td>
                      <td>
                        <span className={`email-category ${getCategoryClass(email.category)}`}>
                          {email.category}
                        </span>
                      </td>
                      <td className="email-date-cell">{formatDate(email.received_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {emails.length === 0 && !loading && (
                <div className="loading">No emails yet. Submit your first email!</div>
              )}
            </div>
          ) : (
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
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
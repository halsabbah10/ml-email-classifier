export interface Email {
  id: number;
  from_address: string;
  subject: string;
  body: string;
  category: 'Billing Issue' | 'Technical Support' | 'Feedback' | 'Other';
  received_at: string;
}

export interface EmailCreate {
  from_address: string;
  subject: string;
  body: string;
}

export interface BatchUploadResponse {
  success_count: number;
  failed_count: number;
  total_count: number;
  failed_emails: Array<{
    email: EmailCreate;
    error: string;
  }>;
  message: string;
}
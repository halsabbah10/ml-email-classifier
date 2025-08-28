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
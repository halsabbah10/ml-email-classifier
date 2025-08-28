import axios from 'axios';
import { Email, EmailCreate, BatchUploadResponse } from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const emailApi = {
  createEmail: async (email: EmailCreate): Promise<Email> => {
    const response = await api.post<Email>('/api/emails', email);
    return response.data;
  },

  uploadJsonFiles: async (files: FileList): Promise<BatchUploadResponse> => {
    const formData = new FormData();
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });

    const response = await api.post<BatchUploadResponse>('/api/emails/upload-json', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getEmails: async (skip = 0, limit = 100): Promise<Email[]> => {
    const response = await api.get<Email[]>('/api/emails', {
      params: { skip, limit },
    });
    return response.data;
  },

  getEmail: async (id: number): Promise<Email> => {
    const response = await api.get<Email>(`/api/emails/${id}`);
    return response.data;
  },
};
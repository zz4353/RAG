export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: Document[];
}

export interface Document {
  id: string;
  title: string;
  content: string;
  score?: number;
  source?: string;
}

export interface ChatResponse {
  answer: string;
  sources: Document[];
  query_type: 'vector' | 'graph' | 'hybrid';
}

export interface UploadResponse {
  message: string;
  documents_processed: number;
  collection_name: string;
}

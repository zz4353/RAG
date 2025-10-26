import { useState, useCallback } from 'react';
import { chatAPI } from '../services/api';
import { Message, ChatResponse } from '../types';

export const useRAG = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (
    message: string, 
    queryType: 'vector' | 'graph' | 'hybrid' = 'hybrid'
  ): Promise<ChatResponse | null> => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatAPI.sendMessage(message, queryType);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Có lỗi xảy ra';
      setError(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const uploadDocuments = useCallback(async (files: File[]) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatAPI.uploadDocuments(files);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Có lỗi xảy ra khi tải lên';
      setError(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    sendMessage,
    uploadDocuments,
    isLoading,
    error,
    clearError: () => setError(null),
  };
};

import axios from 'axios';

// Connects to FastAPI running locally
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const AgenticApi = {
    checkStatus: async () => {
        const response = await apiClient.get('/status');
        return response.data;
    },
    
    ingestPapers: async (query: string, maxResults: number = 5) => {
        const response = await apiClient.post('/ingest', { 
            query, 
            max_results: maxResults 
        });
        return response.data;
    },
    
    conductResearch: async (query: string, retrievalK: number = 10) => {
        const response = await apiClient.post('/research', { 
            query, 
            retrieval_k: retrievalK 
        });
        return response.data;
    },
    
    clearVectorStore: async () => {
        const response = await apiClient.delete('/vectorstore');
        return response.data;
    }
};
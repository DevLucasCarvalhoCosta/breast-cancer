import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://cancermama-backend-868844927948.southamerica-east1.run.app/api',
});

export const getDatasetStats = () => api.get('/data/stats');
export const getSamples = (params?: any) => api.get('/data/samples', { params });
export const getFeatures = () => api.get('/data/features');

export const getMedicalReport = (data: { features_data: any, prediction: int, probability: float }) => 
  api.post('/ai/report', data);

export const getEDASummary = (correlationData: any) => 
  api.post('/ai/eda-summary', { correlation_data: correlationData });

export default api;

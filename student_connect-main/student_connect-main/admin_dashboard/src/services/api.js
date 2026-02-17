import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('adminToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const loginAdmin = (credentials) => api.post('/admin/login', credentials);
export const getOutpasses = () => api.get('/admin/outpasses');
export const updateOutpassStatus = (id, status) => api.put(`/admin/outpasses/${id}`, { status });
export const getTemplateTypes = () => api.get('/admin/templates/list');
export const saveTemplate = (content, type, variables) => api.post('/admin/templates', { content, type, variables });
export const getTemplate = (type = 'outpass') => api.get(`/admin/templates?type=${type}`);

export default api;

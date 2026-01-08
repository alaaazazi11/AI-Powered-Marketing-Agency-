import axios from 'axios';
import { AdContent, BackendAdRequest } from '../types';
import { useNavigate } from 'react-router-dom';


const API_URL = 'http://127.0.0.1:8000';

export const generateAd = async (
  payload: BackendAdRequest
): Promise<AdContent> => {
  try {
    const response = await axios.post(
      `${API_URL}/create_ad`,
      payload
    );
    
    return response.data;
  } catch (error) {
    console.error('Error calling FastAPI:', error);
    throw error;
  }
};



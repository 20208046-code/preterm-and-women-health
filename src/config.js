// Central place for the backend API base URL.
// Override at build time with REACT_APP_API_BASE if you deploy the API elsewhere.
export const API_BASE =
  process.env.REACT_APP_API_BASE || 'http://localhost:5000';

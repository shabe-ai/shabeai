import axios from "axios";
import Cookies from "js-cookie";

const http = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  withCredentials: true,
});

http.interceptors.request.use((config) => {
  const token = Cookies.get("crm-auth");       // ← FastAPI cookie name
  if (token) config.headers["Cookie"] = `crm-auth=${token}`;
  return config;
});

export default http; 
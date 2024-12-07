import axios from 'axios';

// 创建 Axios 实例
const instance = axios.create({
  timeout: 10000, // 请求超时时间（毫秒）
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 在发送请求之前处理，例如添加 Token
    const token = localStorage.getItem('token'); // 从 localStorage 获取 token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`; // 设置 Authorization 请求头
    }

    // 可以在这里添加全局加载动画
    console.log('Request sent:', config);

    return config;
  },
  (error) => {
    // 处理请求错误
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 处理响应数据
    console.log('Response received:', response);

    // 可以在这里关闭全局加载动画
    return response.data; // 直接返回响应的 data
  },
  (error) => {
    // 处理响应错误
    if (error.response) {
      // 服务端返回的错误（如 401、404 等）
      console.error('Response error:', error.response);
      if (error.response.status === 401) {
        // 处理未授权（例如跳转到登录页面）
        window.location.href = '/login';
      }
    } else if (error.request) {
      // 请求未收到响应
      console.error('No response received:', error.request);
    } else {
      // 请求配置错误
      console.error('Request configuration error:', error.message);
    }

    return Promise.reject(error);
  }
);

// 封装通用的请求方法
export const get = (url, params) => instance.get(url, { params });
export const post = (url, data) => instance.post(url, data);
export const put = (url, data) => instance.put(url, data);
export const del = (url) => instance.delete(url);

// 默认导出 Axios 实例
export default instance;

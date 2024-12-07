import { createStore } from 'vuex';
import axios from 'axios'; // 如果您在 utils/request.js 中配置了 axios，可以引入它

const store = createStore({
  state: {
    user: null, // 用户信息
    isAuthenticated: false, // 登录状态
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      state.isAuthenticated = !!user;
    },
    clearUser(state) {
      state.user = null;
      state.isAuthenticated = false;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/api/login', credentials); // 调用后端 API
        commit('setUser', response.data.user);
        return true;
      } catch (error) {
        console.error('登录失败:', error);
        return false;
      }
    },
    async checkLoginStatus({ commit }) {
      try {
        const response = await axios.get('/api/check-auth'); // 调用检查登录状态的 API
        commit('setUser', response.data.user);
      } catch {
        commit('clearUser');
      }
    },
  },
  getters: {
    isAdmin(state) {
      return state.user && state.user.role === 'admin';
    },
    isUser(state) {
      return state.user && state.user.role === 'user';
    },
  },
});

export default store;


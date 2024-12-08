<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../utils/request'

// 路由
const route = useRoute()
const router = useRouter()

// 判断是否是登录或注册页面
const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/register'
})

// 用户名
const username = ref('')

// 如果用户已登录，从本地存储加载用户名
if (localStorage.getItem('username')) {
  username.value = localStorage.getItem('username')
}

// 跳转到 Home 
function goToHome() {
  router.push('/Main')
}

// 跳转到 Admin 
function goToAdmin() {
  router.push('/Admin')
}

// 登出功能
async function logout() {
  try {
    // 调用后端的登出接口
    await request.post('/api/logout');
    
    // 清除本地存储
    localStorage.removeItem('username');
    localStorage.removeItem('token');

    // 跳转到登录页面
    router.push('/login');
    alert('Logged out successfully.');
  } catch (error) {
    console.error('Error during logout:', error);
    alert('An error occurred while logging out. Please try again.');
  }
}

</script>

<template>
  <header class="header">
    <div class="left-section">
      <!-- SVG Logo Start -->
      <div class="logo-container">
        <svg class="logo-svg" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="shipGradient" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#00AEEF"/>
              <stop offset="100%" stop-color="#66CCFF"/>
            </linearGradient>
            <linearGradient id="waveGradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.8"/>
              <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <circle cx="100" cy="100" r="90" fill="url(#shipGradient)" opacity="0.2"/>
          <path d="M50 110 Q100 60 150 110" stroke="url(#shipGradient)" stroke-width="8" fill="none" stroke-linecap="round"/>
          <path d="M60 105 Q100 80 140 105" stroke="url(#shipGradient)" stroke-width="4" fill="none" stroke-linecap="round"/>
          <path d="M115 100 L135 80 L125 100 Z" fill="url(#shipGradient)" opacity="0.9"/>
          <path d="M40 130 Q70 120 100 130 T160 130" stroke="url(#waveGradient)" stroke-width="4" fill="none" stroke-linecap="round"/>
        </svg>
      </div>
      <!-- SVG Logo End -->
      <h1 class="title">Cruise Management System</h1>
    </div>
    <div class="user-info">
      <template v-if="isAuthPage">
        <button class="btn" @click="goToHome">Main</button>
        <button class="btn" @click="goToAdmin">Admin</button>
      </template>
      <template v-else>
        <span class="greeting">Hello, {{ username }}</span>
        <button class="btn" @click="goToHome">Main</button>
        <button class="btn" @click="goToAdmin">Admin</button>
        <button class="logout-btn" @click="logout">Logout</button>
      </template>
    </div>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background: linear-gradient(135deg, #003399, #66ccff);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  position: relative;
}

/* 左侧区域 */
.left-section {
  display: flex;
  align-items: center;
}

/* Logo容器 */
.logo-container {
  width: 50px;
  height: 50px;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-svg {
  width: 100%;
  height: 100%;
}


.title {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(to right, #ffffff, #ccf0ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
  font-family: 'Roboto', sans-serif;
}

/* 用户信息和按钮区域 */
.user-info {
  display: flex;
  align-items: center;
}

.greeting {
  font-size: 16px;
  color: #fff;
  margin-right: 20px;
  font-weight: 500;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.3);
}

/* 按钮样式 */
.btn, .logout-btn {
  padding: 8px 15px;
  font-size: 14px;
  background-color: rgba(255, 255, 255, 0.3);
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  margin-right: 10px;
  transition: all 0.3s ease;
  font-weight: 500;
  font-family: 'Roboto', sans-serif;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.btn:hover, .logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}


.logout-btn {
  background: linear-gradient(135deg, #ff4d4f, #ff6668);
  margin-left: 10px;
  box-shadow: 0 2px 5px rgba(255, 0, 0, 0.3);
}

.logout-btn:hover {
  background: linear-gradient(135deg, #cc0000, #e60000);
}

/* 响应式处理 */
@media (max-width: 600px) {
  .header {
    flex-direction: column;
    text-align: center;
  }

  .left-section {
    margin-bottom: 15px;
  }

  .user-info {
    flex-direction: column;
  }

  .greeting {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .btn, .logout-btn {
    margin-right: 0;
    margin-bottom: 10px;
    width: 100%;
  }
}
</style>

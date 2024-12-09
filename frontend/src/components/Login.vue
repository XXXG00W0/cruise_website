<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import request from '../utils/request'

let loginUser = reactive({
  username: '', 
  password: ''
})

let usernameMsg = ref('')
let passwordMsg = ref('')
let isPasswordVisible = ref(false) 
const router = useRouter()

// 登录方法
async function login() {
  // 基础校验
  if (!checkUsername() || !checkPassword()) {
    alert('Please fix the errors before login.');
    console.log('Validation failed: Username or password is incorrect.');
    return;
  }

  try {
    console.log('Sending login request with username:', loginUser.username);

    // 发送请求
    const response = await request.post('/api/login', {
      username: loginUser.username,
      password: loginUser.password,
    });

    // 打印完整的响应数据
    console.log('Login API response:', response);

    // 检查状态码或响应内容
    if (response && response.message === 'Login successful') {
      alert('Login successfully');
      console.log('Login successful, extracting token and user data.');

      // 提取 token 和 user 数据
      const { token, user } = response; // 假设拦截器已处理返回值
      console.log('Extracted token:', token);
      console.log('Extracted user data:', user);

      // 确保 user 和 user.user_type 存在
      if (!user || !user.user_type) {
        console.error('User data is missing or invalid:', user);
        alert('Login response is invalid. Please try again.');
        return;
      }

      // 将 token 存储到 localStorage 中
      localStorage.setItem('token', token);
      localStorage.setItem('username', user.username);
      console.log('Token stored in localStorage.');
      console.log(user.username);


      // 打印跳转路径
      const navigatePath = user.user_type === 'admin' ? '/Board' : '/Main';
      console.log('Navigating to:', navigatePath);

      // 跳转到对应页面
      try {
        await router.push(navigatePath);
        console.log('Navigation successful to:', navigatePath);
      } catch (navigationError) {
        console.error('Navigation error:', navigationError);
        alert('Failed to navigate. Please try again.');
      }
    } else {
      // 如果状态码或 message 不符合预期，处理错误
      console.error('Unexpected response:', response);
      alert(response.message || 'Login failed');
    }
  } catch (err) {
    // 捕获请求或其他错误
    console.error('Error during login:', err.response ? err.response.data : err.message);
    alert('An error occurred. Please try again.');
  }
}


// 验证用户名方法
function checkUsername() {
  if (!loginUser.username) {
    usernameMsg.value = 'Username cannot be empty'
    return false
  }
  usernameMsg.value = 'Valid'
  return true
}

// 验证密码方法
function checkPassword() {
  if (!loginUser.password) {
    passwordMsg.value = 'Password cannot be empty'
    return false
  }
  passwordMsg.value = 'Valid'
  return true
}

// 切换密码可见性
function togglePasswordVisibility() {
  isPasswordVisible.value = !isPasswordVisible.value
}

// 重置表单
function resetForm() {
  loginUser.username = ''
  loginUser.password = ''
  usernameMsg.value = ''
  passwordMsg.value = ''
}
</script>

<template>
  <div class="page-background">
    <div class="overlay">
      <div class="login-container">
        <h3 class="header">Login</h3>
        <div class="form-container">
          <table class="form-table">
            <!-- 用户名输入 -->
            <tr>
              <td class="label">Username:</td>
              <td>
                <input
                  class="input"
                  type="text"
                  v-model="loginUser.username"
                  @blur="checkUsername()"
                  placeholder="Enter your username"
                />
              </td>
            </tr>
            <tr>
              <td colspan="2">
                <span :class="['message', usernameMsg === 'Valid' ? 'valid' : 'invalid']" v-text="usernameMsg"></span>
              </td>
            </tr>
            <!-- 密码输入 -->
            <tr>
              <td class="label">Password:</td>
              <td class="password-field">
                <input
                  class="input"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  v-model="loginUser.password"
                  @blur="checkPassword()"
                  placeholder="Enter your password"
                />
                <button class="toggle-visibility-btn" @click="togglePasswordVisibility()">
                  {{ isPasswordVisible ? 'Hide' : 'Show' }}
                </button>
              </td>
            </tr>
            <tr>
              <td colspan="2">
                <span :class="['message', passwordMsg === 'Valid' ? 'valid' : 'invalid']" v-text="passwordMsg"></span>
              </td>
            </tr>
            <!-- 按钮 -->
            <tr>
              <td colspan="2" class="button-container">
                <button class="btn login-btn" @click="login()">Login</button>
                <button class="btn reset-btn" @click="resetForm()">Reset</button>
                <router-link to="/regist">
                  <button class="btn register-btn">Register</button>
                </router-link>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面背景及布局 */
.page-background {
  width: 100vw;
  height: 100vh;
  background-image: url('../assets/img/cruise_ship.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Roboto', sans-serif;
  position: relative;
}

.overlay {
  background-color: rgba(0, 0, 0, 0.4);
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 容器样式 */
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 15px;
  width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* 标题样式 */
.header {
  color: #007acc;
  font-size: 28px;
  margin-bottom: 20px;
  font-weight: bold;
}

/* 表单容器样式 */
.form-container {
  width: 100%;
}

/* 表格样式 */
.form-table {
  width: 100%;
  border-collapse: collapse;
}

.label {
  text-align: right;
  padding-right: 10px;
  font-size: 16px;
  color: #333;
  width: 30%;
  white-space: nowrap;
}

.input {
  width: 90%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease;
  font-size: 14px;
}

.input:focus {
  border-color: #007acc;
  outline: none;
  background-color: #f0f9ff;
}

.password-field {
  display: flex;
  align-items: center;
}

.toggle-visibility-btn {
  margin-left: 10px;
  background-color: transparent;
  border: none;
  color: #007acc;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.3s;
}

.toggle-visibility-btn:hover {
  color: #005f99;
  text-decoration: underline;
}

/* 提示信息样式 */
.message {
  font-size: 13px;
  margin-top: 5px;
  display: block;
  text-align: left;
  font-weight: bold;
}

.message.valid {
  color: #28a745;
}

.message.invalid {
  color: #ff6f61;
}

/* 按钮样式 */
.button-container {
  text-align: center;
  padding-top: 15px;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 5px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  outline: none;
}

.btn:hover {
  transform: translateY(-2px);
}

.login-btn {
  background-color: #007acc;
}

.login-btn:hover {
  background-color: #005f99;
}

.reset-btn {
  background-color: #ffc107;
  color: #333;
}

.reset-btn:hover {
  background-color: #e6a700;
}

.register-btn {
  background-color: #28a745;
}

.register-btn:hover {
  background-color: #218838;
}
</style>

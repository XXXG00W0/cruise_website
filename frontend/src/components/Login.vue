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
    alert('Please fix the errors before login.')
    return
  }

  try {
    const response = await request.post('/api/login', {
      username: loginUser.username,
      password: loginUser.password
    })

    // response成功返回时的结构：status 200表示成功，否则失败
    if (response.status === 200) {
      alert('Login successfully')

      // 从返回数据中提取 token 和 user 信息
      const token = response.data.token
      const user = response.data.user

      // 将token存储在localStorage中，供后续API请求使用
      localStorage.setItem('token', token)

      // 根据用户角色跳转
      if (user.user_type === 'admin') {
        router.push('/Board')
      } else {
        router.push('/Main')
      }
    } else {
      alert(response.message || 'Login failed')
    }
  } catch (err) {
    console.error(err)
    alert('An error occurred. Please try again.')
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

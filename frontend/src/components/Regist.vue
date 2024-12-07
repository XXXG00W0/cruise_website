<script setup>
import { ref, reactive } from 'vue'
import request from '../utils/request'
import { useRouter } from 'vue-router'

const router = useRouter()

// 国家列表（示例）
const validCountries = ['China', 'United States', 'Canada', 'France', 'Germany', 'Japan', 'United Kingdom', 'Australia']

// 添加地址相关字段
let registUser = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  first_name: '',
  last_name: '',
  birth_date: '',  // YYYY-MM-DD 格式
  gender: '', // 下拉框选择
  nationality: '',
  phone: '',
  group_id: '',
  street: '',
  addr_line_2: '', // optional
  neighborhood: '',
  city: '',
  state_province: '',
  postal_code: '',
  country: ''
})

let usernameMsg = ref('')
let emailMsg = ref('')
let passwordMsg = ref('')
let confirmPasswordMsg = ref('')
let firstNameMsg = ref('')
let lastNameMsg = ref('')
let birthDateMsg = ref('')
let genderMsg = ref('')
let nationalityMsg = ref('')
let phoneMsg = ref('')
// 地址相关信息
let streetMsg = ref('')
// addr_line_2可选，不严格检查
let neighborhoodMsg = ref('')
let cityMsg = ref('')
let stateProvinceMsg = ref('')
let postalCodeMsg = ref('')
let countryMsg = ref('')

let isPasswordVisible = ref(false)

function checkField(value, message, condition = true) {
  if (!value || !condition) {
    return message
  }
  return 'Valid'
}

function checkUsername() {
  usernameMsg.value = checkField(
    registUser.username,
    'Username must be at least 5 characters',
    registUser.username && registUser.username.length >= 5
  )
  return usernameMsg.value === 'Valid'
}

function checkEmail() {
  const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  emailMsg.value = checkField(
    registUser.email,
    'Invalid email format',
    emailReg.test(registUser.email)
  )
  return emailMsg.value === 'Valid'
}

function checkPassword() {
  const strongPasswordReg = /^(?=.*[A-Z])(?=.*\d).{8,}$/
  passwordMsg.value = checkField(
    registUser.password,
    'Password must be at least 8 characters, include one uppercase letter and one number',
    strongPasswordReg.test(registUser.password)
  )
  return passwordMsg.value === 'Valid'
}

function checkConfirmPassword() {
  confirmPasswordMsg.value = checkField(
    registUser.confirm_password,
    'Passwords do not match',
    registUser.password === registUser.confirm_password
  )
  return confirmPasswordMsg.value === 'Passwords match'
}

function checkFirstName() {
  firstNameMsg.value = checkField(
    registUser.first_name,
    'First name cannot be empty'
  )
  return firstNameMsg.value === 'Valid'
}

function checkLastName() {
  lastNameMsg.value = checkField(
    registUser.last_name,
    'Last name cannot be empty'
  )
  return lastNameMsg.value === 'Valid'
}

function checkBirthDate() {
  const birthDateReg = /^\d{4}-\d{2}-\d{2}$/
  birthDateMsg.value = checkField(
    registUser.birth_date,
    'Birth date must be in YYYY-MM-DD format',
    birthDateReg.test(registUser.birth_date)
  )
  return birthDateMsg.value === 'Valid'
}

function checkGender() {
  // 选择性别
  genderMsg.value = checkField(
    registUser.gender,
    'Please select a gender',
    ['Male', 'Female','other'].includes(registUser.gender)
  )
  return genderMsg.value === 'Valid'
}

function checkNationality() {
  // 检查输入的国籍是否在已知国家列表中
  nationalityMsg.value = checkField(
    registUser.nationality,
    'Invalid nationality. Please enter a real country name.',
    validCountries.includes(registUser.nationality)
  )
  return nationalityMsg.value === 'Valid'
}

function checkPhone() {
  const phoneReg = /^\+?\d{10,15}$/
  phoneMsg.value = checkField(
    registUser.phone,
    'Phone number must be a valid format (e.g., +1234567890)',
    phoneReg.test(registUser.phone)
  )
  return phoneMsg.value === 'Valid'
}

// 地址字段检查（除 addr_line_2外皆必填）
function checkStreet() {
  streetMsg.value = checkField(
    registUser.street,
    'Street cannot be empty'
  )
  return streetMsg.value === 'Valid'
}

function checkNeighborhood() {
  neighborhoodMsg.value = checkField(
    registUser.neighborhood,
    'Neighborhood cannot be empty'
  )
  return neighborhoodMsg.value === 'Valid'
}

function checkCity() {
  cityMsg.value = checkField(
    registUser.city,
    'City cannot be empty'
  )
  return cityMsg.value === 'Valid'
}

function checkStateProvince() {
  stateProvinceMsg.value = checkField(
    registUser.state_province,
    'State/Province cannot be empty'
  )
  return stateProvinceMsg.value === 'Valid'
}

function checkPostalCode() {
  postalCodeMsg.value = checkField(
    registUser.postal_code,
    'Postal Code cannot be empty'
  )
  return postalCodeMsg.value === 'Valid'
}

function checkCountry() {
  countryMsg.value = checkField(
    registUser.country,
    'Country cannot be empty'
  )
  return countryMsg.value === 'Valid'
}

// 切换密码可见性
function togglePasswordVisibility() {
  isPasswordVisible.value = !isPasswordVisible.value
}

// 注册方法
async function regist() {
  // 检查所有必填字段
  const validations = [
    checkUsername,
    checkEmail,
    checkPassword,
    checkConfirmPassword,
    checkFirstName,
    checkLastName,
    checkBirthDate,
    checkGender,
    checkNationality,
    checkPhone,
    checkStreet,
    checkNeighborhood,
    checkCity,
    checkStateProvince,
    checkPostalCode,
    checkCountry
    // group_id可选，不检查
    // addr_line_2可空，不检查
  ]

  // 检查所有字段
  const isValid = validations.every((validate) => validate())

  if (isValid) {
    try {
      const response = await request.post('http://127.0.0.1:5000/register', {
        username: registUser.username,
        email: registUser.email,
        password: registUser.password,
        confirm_password: registUser.confirm_password,
        first_name: registUser.first_name,
        last_name: registUser.last_name,
        birth_date: registUser.birth_date,
        gender: registUser.gender,
        nationality: registUser.nationality,
        phone: registUser.phone,
        group_id: registUser.group_id || null,
        street: registUser.street,
        addr_line_2: registUser.addr_line_2,
        neighborhood: registUser.neighborhood,
        city: registUser.city,
        state_province: registUser.state_province,
        postal_code: registUser.postal_code,
        country: registUser.country
      })

      if (response.status === 201) {
        alert('Registration successful! You can now log in.')
        router.push('/login')
      } else {
        alert(response.data.message || 'Register failed')
      }
    } catch (err) {
      console.error(err)
      alert('An error occurred during registration. Please try again.')
    }
  } else {
    alert('Please fix the errors before registration.')
  }
}
</script>

<template>
  <div class="page-background">
    <div class="overlay">
      <div class="register-container">
        <h3 class="header">Register</h3>
        <div class="form-container">
          <table class="form-table">

            <!-- 用户名 -->
            <tr>
              <td class="label">Username:</td>
              <td>
                <input class="input" type="text" v-model="registUser.username" @blur="checkUsername()" placeholder="Enter username" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', usernameMsg === 'Valid' ? 'valid' : 'invalid']">{{ usernameMsg }}</span></td></tr>

            <!-- 邮箱 -->
            <tr>
              <td class="label">Email:</td>
              <td>
                <input class="input" type="email" v-model="registUser.email" @blur="checkEmail()" placeholder="Enter email" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', emailMsg === 'Valid' ? 'valid' : 'invalid']">{{ emailMsg }}</span></td></tr>

            <!-- 密码 -->
            <tr>
              <td class="label">Password:</td>
              <td class="password-field">
                <input class="input" :type="isPasswordVisible ? 'text' : 'password'" v-model="registUser.password" @blur="checkPassword()" placeholder="Enter password" />
                <button class="toggle-visibility-btn" @click="togglePasswordVisibility()">{{ isPasswordVisible ? 'Hide' : 'Show' }}</button>
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', passwordMsg === 'Valid' ? 'valid' : 'invalid']">{{ passwordMsg }}</span></td></tr>

            <!-- 确认密码 -->
            <tr>
              <td class="label">Confirm Password:</td>
              <td>
                <input class="input" type="password" v-model="registUser.confirm_password" @blur="checkConfirmPassword()" placeholder="Confirm password" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', confirmPasswordMsg === 'Passwords match' ? 'valid' : 'invalid']">{{ confirmPasswordMsg }}</span></td></tr>

            <!-- First Name -->
            <tr>
              <td class="label">First Name:</td>
              <td>
                <input class="input" type="text" v-model="registUser.first_name" @blur="checkFirstName()" placeholder="Enter first name" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', firstNameMsg === 'Valid' ? 'valid' : 'invalid']">{{ firstNameMsg }}</span></td></tr>

            <!-- Last Name -->
            <tr>
              <td class="label">Last Name:</td>
              <td>
                <input class="input" type="text" v-model="registUser.last_name" @blur="checkLastName()" placeholder="Enter last name" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', lastNameMsg === 'Valid' ? 'valid' : 'invalid']">{{ lastNameMsg }}</span></td></tr>

            <!-- Birth Date -->
            <tr>
              <td class="label">Birth Date:</td>
              <td>
                <input class="input" type="date" v-model="registUser.birth_date" @blur="checkBirthDate()" placeholder="YYYY-MM-DD" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', birthDateMsg === 'Valid' ? 'valid' : 'invalid']">{{ birthDateMsg }}</span></td></tr>

            <!-- Gender 下拉框选择 -->
            <tr>
              <td class="label">Gender:</td>
              <td>
                <select class="input" v-model="registUser.gender" @blur="checkGender()">
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="other">Other</option>
                </select>
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', genderMsg === 'Valid' ? 'valid' : 'invalid']">{{ genderMsg }}</span></td></tr>

            <!-- Nationality -->
            <tr>
              <td class="label">Nationality:</td>
              <td>
                <input class="input" type="text" v-model="registUser.nationality" @blur="checkNationality()" placeholder="Enter nationality (e.g. China, United States...)" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', nationalityMsg === 'Valid' ? 'valid' : 'invalid']">{{ nationalityMsg }}</span></td></tr>

            <!-- Phone -->
            <tr>
              <td class="label">Phone:</td>
              <td>
                <input class="input" type="text" v-model="registUser.phone" @blur="checkPhone()" placeholder="Enter phone number" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', phoneMsg === 'Valid' ? 'valid' : 'invalid']">{{ phoneMsg }}</span></td></tr>

            <!-- Street -->
            <tr>
              <td class="label">Street:</td>
              <td>
                <input class="input" type="text" v-model="registUser.street" @blur="checkStreet()" placeholder="Enter street" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', streetMsg === 'Valid' ? 'valid' : 'invalid']">{{ streetMsg }}</span></td></tr>

            <!-- Addr_line_2 (可选) -->
            <tr>
              <td class="label">Address Line 2 (optional):</td>
              <td>
                <input class="input" type="text" v-model="registUser.addr_line_2" placeholder="Enter address line 2 if any" />
              </td>
            </tr>

            <!-- Neighborhood -->
            <tr>
              <td class="label">Neighborhood:</td>
              <td>
                <input class="input" type="text" v-model="registUser.neighborhood" @blur="checkNeighborhood()" placeholder="Enter neighborhood" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', neighborhoodMsg === 'Valid' ? 'valid' : 'invalid']">{{ neighborhoodMsg }}</span></td></tr>

            <!-- City -->
            <tr>
              <td class="label">City:</td>
              <td>
                <input class="input" type="text" v-model="registUser.city" @blur="checkCity()" placeholder="Enter city" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', cityMsg === 'Valid' ? 'valid' : 'invalid']">{{ cityMsg }}</span></td></tr>

            <!-- State Province -->
            <tr>
              <td class="label">State/Province:</td>
              <td>
                <input class="input" type="text" v-model="registUser.state_province" @blur="checkStateProvince()" placeholder="Enter state or province" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', stateProvinceMsg === 'Valid' ? 'valid' : 'invalid']">{{ stateProvinceMsg }}</span></td></tr>

            <!-- Postal Code -->
            <tr>
              <td class="label">Postal Code:</td>
              <td>
                <input class="input" type="text" v-model="registUser.postal_code" @blur="checkPostalCode()" placeholder="Enter postal code" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', postalCodeMsg === 'Valid' ? 'valid' : 'invalid']">{{ postalCodeMsg }}</span></td></tr>

            <!-- Country -->
            <tr>
              <td class="label">Country:</td>
              <td>
                <input class="input" type="text" v-model="registUser.country" @blur="checkCountry()" placeholder="Enter country" />
              </td>
            </tr>
            <tr><td colspan="2"><span :class="['message', countryMsg === 'Valid' ? 'valid' : 'invalid']">{{ countryMsg }}</span></td></tr>

            <!-- Group ID (可选) -->
            <tr>
              <td class="label">Group ID (optional):</td>
              <td>
                <input class="input" type="number" v-model="registUser.group_id" placeholder="Enter group ID if any" />
              </td>
            </tr>

            <!-- 按钮 -->
            <tr>
              <td colspan="2" class="button-container">
                <button class="btn register-btn" @click="regist()">Register</button>
                <router-link to="/login">
                  <button class="btn login-btn">Back to Login</button>
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
/* 样式同之前版本，不再重复解释 */
.page-background {
  width: 100vw;
  height: 100vh;
  background: url('../assets/img/register_background.png') no-repeat center center/cover; 
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  font-family: 'Roboto', sans-serif;
}

.overlay {
  background: rgba(0,0,0,0.4);
  width: 100%;
  height: 100%;
  position: absolute;
  top:0; left:0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255, 255, 255, 0.9); 
  padding: 30px;
  border-radius: 15px;
  width: 450px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 10;
}

.header {
  color: #007acc;
  font-size: 28px;
  margin-bottom: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

.form-container {
  width: 100%;
}

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
  vertical-align: top;
}

.input {
  width: 80%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  font-size: 14px;
  margin-bottom: 5px;
}

.input:focus {
  border-color: #66ccff;
  outline: none;
  background-color: #f0f9ff;
  box-shadow: 0 0 8px rgba(102,204,255,0.3);
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

.button-container {
  text-align: center;
  padding-top: 15px;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  margin: 5px;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  font-weight: 500;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.register-btn {
  background: linear-gradient(135deg, #28a745, #5cd75c);
}

.register-btn:hover {
  background: linear-gradient(135deg, #218838, #4ec94e);
}

.login-btn {
  background: linear-gradient(135deg, #007acc, #66ccff);
}

.login-btn:hover {
  background: linear-gradient(135deg, #005f99, #40b6ff);
}

@media (max-width: 600px) {
  .register-container {
    width: 90%;
    padding: 20px;
  }

  .label {
    text-align: left;
    padding-right: 0;
    margin-bottom: 5px;
  }

  .form-table tr {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
  }

  .form-table td {
    width: 100%;
  }

  .button-container {
    display: flex;
    flex-direction: column;
  }

  .btn {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>

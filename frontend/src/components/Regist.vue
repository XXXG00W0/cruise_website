<script setup>
import { ref, reactive } from 'vue'
import request from '../utils/request'
import { useRouter } from 'vue-router'

const router = useRouter()

const validCountries = [
  'China',
  'India',
  'United States',
  'Canada',
  'France',
  'Germany',
  'Japan',
  'United Kingdom',
  'Australia',
  'Mexico',
  'Russia',
  'South Korea',
  'Italy',
  'Spain',
  'Indonesia',
  'Netherlands',
  'Turkey',
  'Saudi Arabia',
  'Switzerland',
  'Sweden',
  'Poland',
  'Belgium',
  'Norway',
  'Austria',
  'Denmark',
  'Singapore',
  'Finland',
  'Chile',
  'Brazil',
  'Argentina',
  'South Africa',
  'Egypt',
  'Nigeria',
  'Kenya',
  'Morocco',
  'Ghana',
  'Tunisia',
  'Vietnam',
  'Thailand',
  'Philippines',
  'Malaysia',
  'New Zealand',
  'Pakistan',
  'Bangladesh',
  'Sri Lanka',
  'Myanmar',
  'Cambodia',
  'Laos'
];

let registUser = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  first_name: '',
  last_name: '',
  birth_date: '', // YYYY-MM-DD 格式
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
});

let usernameMsg = ref('')
let emailMsg = ref('')
let passwordMsg = ref('')
let confirmPasswordMsg = ref('')
let firstNameMsg = ref('')
let lastNameMsg = ref('')
let birthDateMsg = ref('')
let genderMsg = ref('')
let phoneMsg = ref('')
// 地址相关信息
let streetMsg = ref('')
// addr_line_2可选，不严格检查
let neighborhoodMsg = ref('')
let cityMsg = ref('')
let stateProvinceMsg = ref('')
let postalCodeMsg = ref('')
let nationalityMsg = ref('');
let countryMsg = ref('');

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
  return confirmPasswordMsg.value === 'Valid' 
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
    ['male', 'female','other'].includes(registUser.gender)
  )
  return genderMsg.value === 'Valid'
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

function checkNationality() {
  nationalityMsg.value = checkField(
    registUser.nationality,
    'Please select a nationality',
    validCountries.includes(registUser.nationality)
  );
  return nationalityMsg.value === 'Valid';
}

function checkCountry() {
  countryMsg.value = checkField(
    registUser.country,
    'Please select a country',
    validCountries.includes(registUser.country)
  );
  return countryMsg.value === 'Valid';
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
      const response = await request.post('/api/register', {
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
        alert(response.message || 'Register failed')
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
          <div class="form-row">
            <div class="form-column">
              <!-- Username -->
              <div class="form-group">
                <label class="label">Username:</label>
                <input class="input" type="text" v-model="registUser.username" @blur="checkUsername()" placeholder="Enter username" />
                <span :class="['message', usernameMsg === 'Valid' ? 'valid' : 'invalid']">{{ usernameMsg }}</span>
              </div>

              <!-- Email -->
              <div class="form-group">
                <label class="label">Email:</label>
                <input class="input" type="email" v-model="registUser.email" @blur="checkEmail()" placeholder="Enter email" />
                <span :class="['message', emailMsg === 'Valid' ? 'valid' : 'invalid']">{{ emailMsg }}</span>
              </div>

              <!-- Password -->
              <div class="form-group">
                <label class="label">Password:</label>
                <div class="password-field">
                  <input class="input" :type="isPasswordVisible ? 'text' : 'password'" v-model="registUser.password" @blur="checkPassword()" placeholder="Enter password" />
                  <button class="toggle-visibility-btn" @click="togglePasswordVisibility()">{{ isPasswordVisible ? 'Hide' : 'Show' }}</button>
                </div>
                <span :class="['message', passwordMsg === 'Valid' ? 'valid' : 'invalid']">{{ passwordMsg }}</span>
              </div>

              <!-- Confirm Password -->
              <div class="form-group">
                <label class="label">Confirm Password:</label>
                <input class="input" type="password" v-model="registUser.confirm_password" @blur="checkConfirmPassword()" placeholder="Confirm password" />
                <span :class="['message', confirmPasswordMsg === 'Valid' ? 'valid' : 'invalid']">{{ confirmPasswordMsg }}</span>
              </div>

              <!-- First Name -->
              <div class="form-group">
                <label class="label">First Name:</label>
                <input class="input" type="text" v-model="registUser.first_name" @blur="checkFirstName()" placeholder="Enter first name" />
                <span :class="['message', firstNameMsg === 'Valid' ? 'valid' : 'invalid']">{{ firstNameMsg }}</span>
              </div>

              <!-- Last Name -->
              <div class="form-group">
                <label class="label">Last Name:</label>
                <input class="input" type="text" v-model="registUser.last_name" @blur="checkLastName()" placeholder="Enter last name" />
                <span :class="['message', lastNameMsg === 'Valid' ? 'valid' : 'invalid']">{{ lastNameMsg }}</span>
              </div>
            </div>

            <div class="form-column">
              <!-- Birth Date -->
              <div class="form-group">
                <label class="label">Birth Date:</label>
                <input class="input" type="date" v-model="registUser.birth_date" @blur="checkBirthDate()" placeholder="YYYY-MM-DD" />
                <span :class="['message', birthDateMsg === 'Valid' ? 'valid' : 'invalid']">{{ birthDateMsg }}</span>
              </div>

              <!-- Gender -->
              <div class="form-group">
                <label class="label">Gender:</label>
                <select class="input" v-model="registUser.gender" @blur="checkGender()">
                  <option value="">Select Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
                <span :class="['message', genderMsg === 'Valid' ? 'valid' : 'invalid']">{{ genderMsg }}</span>
              </div>

              <!-- Nationality -->
              <div class="form-group">
                <label class="label">Nationality:</label>
                <select class="input" v-model="registUser.nationality" @blur="checkNationality()">
                  <option value="">Select Nationality</option>
                  <option v-for="country in validCountries" :key="country" :value="country">
                    {{ country }}
                  </option>
                </select>
                <span :class="['message', nationalityMsg === 'Valid' ? 'valid' : 'invalid']">{{ nationalityMsg }}</span>
              </div>

              <!-- Phone -->
              <div class="form-group">
                <label class="label">Phone:</label>
                <input class="input" type="text" v-model="registUser.phone" @blur="checkPhone()" placeholder="Enter phone number" />
                <span :class="['message', phoneMsg === 'Valid' ? 'valid' : 'invalid']">{{ phoneMsg }}</span>
              </div>

              <!-- Street -->
              <div class="form-group">
                <label class="label">Street:</label>
                <input class="input" type="text" v-model="registUser.street" @blur="checkStreet()" placeholder="Enter street" />
                <span :class="['message', streetMsg === 'Valid' ? 'valid' : 'invalid']">{{ streetMsg }}</span>
              </div>

              <!-- City -->
              <div class="form-group">
                <label class="label">City:</label>
                <input class="input" type="text" v-model="registUser.city" @blur="checkCity()" placeholder="Enter city" />
                <span :class="['message', cityMsg === 'Valid' ? 'valid' : 'invalid']">{{ cityMsg }}</span>
              </div>

              <!-- State/Province -->
              <div class="form-group">
                <label class="label">State/Province:</label>
                <input class="input" type="text" v-model="registUser.state_province" @blur="checkStateProvince()" placeholder="Enter state or province" />
                <span :class="['message', stateProvinceMsg === 'Valid' ? 'valid' : 'invalid']">{{ stateProvinceMsg }}</span>
              </div>
            </div>
          </div>
          <div class="button-container">
            <button class="btn register-btn" @click="regist">Register</button>
            <router-link to="/login">
              <button class="btn login-btn">Back to Login</button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-background {
  width: 100vw;
  height: 100vh;
  background: url('../assets/img/register_background.png') no-repeat center center/cover; 
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 修改位置，避免与 header 冲突 */
  padding-top: 80px; /* 添加顶部间距 */
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
  width: 80%;
  max-width: 900px;
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

.form-row {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.form-column {
  flex: 1;
  min-width: 300px;
  margin: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.label {
  display: block;
  font-size: 16px;
  color: #333;
  margin-bottom: 5px;
}

.input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  font-size: 14px;
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
  margin-top: 20px;
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
  .form-row {
    flex-direction: column;
  }

  .form-column {
    min-width: 100%;
  }

  .register-container {
    width: 90%;
    padding: 20px;
  }

  .btn {
    width: 100%;
  }
}
</style>

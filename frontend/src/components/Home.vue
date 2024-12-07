<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../utils/request'

const activeMenu = ref('Personal Info') // 默认选中 Personal Info

// 数据存储
const dataStore = reactive({
  passenger: null,
  address: null,
  group: null,
  stateroomBooking: [],
  payment: [],
  invoices: {},
  trip: null,
  restaurant: [],
  entertainment: [],
  port: [],
  stateroom: [],
  stateroomPrices: {},
  packages: [],
  searchResults: [] // 存储搜索结果
})

// 编辑个人信息表单数据
const editForm = reactive({
  phone: '',
  street: '',
  city: '',
  state_province: '',
  postal_code: '',
  country: ''
})

const showEditModal = ref(false) // 是否显示编辑个人信息的Modal

// 房间预订相关
const showBookingModal = ref(false)
const bookingForm = reactive({
  stateroomId: null,
  startDate: '',
  endDate: ''
})

// 购买Package相关
const showPurchaseModal = ref(false)
const selectedPackage = ref(null)

// 搜索相关字段
const searchForm = reactive({
  port: '',
  ship: '',
  date: ''
})

onMounted(() => {
  fetchPassengerInfo()
})

// 切换菜单项时动态加载数据
async function switchMenu(menu) {
  activeMenu.value = menu
  if (menu === 'Personal Info' && !dataStore.passenger) {
    await fetchPassengerInfo()
  } else if (menu === 'Group Member' && !dataStore.group) {
    await fetchGroupInfo()
  } else if (menu === 'View My Trip' && !dataStore.trip) {
    await fetchTripInfo()
  } else if (menu === 'Package Service' && dataStore.packages.length === 0) {
    await fetchPackageInfo()
  } 
}

// 获取 Passenger 信息
async function fetchPassengerInfo() {
  try {
    const response = await request.get('/api/passenger-info')
    if (response.code === 200) {
      dataStore.passenger = response.data.passenger
      dataStore.address = response.data.address 
      // 初始化编辑表单数据
      if (dataStore.passenger) {
        editForm.phone = dataStore.passenger.phone || ''
      }
      if (dataStore.address) {
        editForm.street = dataStore.address.street || ''
        editForm.city = dataStore.address.city || ''
        editForm.state_province = dataStore.address.state_province || ''
        editForm.postal_code = dataStore.address.postal_code || ''
        editForm.country = dataStore.address.country || ''
      }
    } else {
      alert('Failed to fetch passenger info')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching passenger info')
  }
}

// 获取 Group 信息
async function fetchGroupInfo() {
  try {
    const response = await request.get('/api/group-info')
    if (response.code === 200) {
      dataStore.group = response.data.group
      dataStore.stateroomBooking = response.data.stateroomBooking
      dataStore.payment = response.data.payment
    } else {
      alert('Failed to fetch group info')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching group info')
  }
}

// 获取 Invoice 信息
async function fetchInvoice(paymentId) {
  if (dataStore.invoices[paymentId]) return 
  try {
    const response = await request.get(`/api/invoice/${paymentId}`)
    if (response.code === 200) {
      dataStore.invoices[paymentId] = response.data.invoice
    } else {
      alert('Failed to fetch invoice')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching invoice')
  }
}

// 获取 Trip 信息
async function fetchTripInfo() {
  try {
    const response = await request.get('/api/trip-info')
    if (response.code === 200) {
      dataStore.trip = response.data.trip
      dataStore.restaurant = response.data.restaurant
      dataStore.entertainment = response.data.entertainment
      dataStore.port = response.data.port
      dataStore.stateroom = response.data.stateroom
    } else {
      alert('Failed to fetch trip info')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching trip info')
  }
}

// 获取 Stateroom Price 信息
async function fetchStateroomPrice(stateroomId) {
  if (dataStore.stateroomPrices[stateroomId]) return 
  try {
    const response = await request.get(`/api/stateroom-price/${stateroomId}`)
    if (response.code === 200) {
      dataStore.stateroomPrices[stateroomId] = response.data.price
    } else {
      alert('Failed to fetch stateroom price')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching stateroom price')
  }
}

// 获取 Package 信息
async function fetchPackageInfo() {
  try {
    const response = await request.get('/api/packages')
    if (response.code === 200) {
      dataStore.packages = response.data.packages
    } else {
      alert('Failed to fetch package information')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching package information')
  }
}

// 更新个人信息
async function updatePersonalInfo() {
  try {
    const response = await request.put('/api/update-passenger-info', {
      phone: editForm.phone,
      address: {
        street: editForm.street,
        city: editForm.city,
        state_province: editForm.state_province,
        postal_code: editForm.postal_code,
        country: editForm.country,
      }
    })
    if (response.code === 200) {
      alert('Personal info updated successfully')
      // 更新前端数据
      if (dataStore.passenger) {
        dataStore.passenger.phone = editForm.phone
      }
      if (dataStore.address) {
        dataStore.address.street = editForm.street
        dataStore.address.city = editForm.city
        dataStore.address.state_province = editForm.state_province
        dataStore.address.postal_code = editForm.postal_code
        dataStore.address.country = editForm.country
      }
      showEditModal.value = false
    } else {
      alert(response.message || 'Failed to update personal info')
    }
  } catch (err) {
    console.error(err)
    alert('Error updating personal info')
  }
}

// 预订房间
async function bookStateroom() {
  try {
    const response = await request.post('/api/book-stateroom', {
      stateroomId: bookingForm.stateroomId,
      startDate: bookingForm.startDate,
      endDate: bookingForm.endDate
    })
    if (response.code === 200) {
      alert('Stateroom booked successfully')
      showBookingModal.value = false
    } else {
      alert(response.message || 'Failed to book stateroom')
    }
  } catch (err) {
    console.error(err)
    alert('Error booking stateroom')
  }
}

// 购买 Package
async function purchasePackage() {
  if (!selectedPackage.value) return
  try {
    const response = await request.post('/api/purchase-package', {
      packageId: selectedPackage.value.packageId
    })
    if (response.code === 200) {
      alert('Package purchased successfully')
      showPurchaseModal.value = false
    } else {
      alert(response.message || 'Failed to purchase package')
    }
  } catch (err) {
    console.error(err)
    alert('Error purchasing package')
  }
}

// 打开预订房间的对话框
function openBookingModal(stateroom) {
  bookingForm.stateroomId = stateroom.stateroomId
  bookingForm.startDate = ''
  bookingForm.endDate = ''
  showBookingModal.value = true
}

// 打开购买Package的对话框
function openPurchaseModal(pkg) {
  selectedPackage.value = pkg
  showPurchaseModal.value = true
}

// 搜索Trip
async function searchTrip() {
  try {
    const response = await request.get('/api/search-trip', {
      params: {
        port: searchForm.port,
        ship: searchForm.ship,
        date: searchForm.date
      }
    })
    if (response.code === 200) {
      dataStore.searchResults = response.data.results
    } else {
      alert(response.message || 'Failed to search trip')
    }
  } catch (err) {
    console.error(err)
    alert('Error searching trip')
  }
}
</script>

<template>
  <div class="home-page">
    <div class="sidebar">
      <h3 class="sidebar-header">Menu</h3>
      <ul class="menu">
        <li
          v-for="menu in ['Search For Trip','Personal Info', 'Group Member', 'View My Trip', 'Package Service']"
          :key="menu"
          :class="{ active: activeMenu === menu }"
          @click="switchMenu(menu)"
        >
          {{ menu }}
        </li>
      </ul>
    </div>
    <div class="content">
      <!-- 搜索栏，当Search For Trip时显示 -->
      <div v-if="activeMenu === 'Search For Trip'" class="search-bar">
        <div class="search-fields">
          <div class="field">
            <label>Port</label>
            <input v-model="searchForm.port" placeholder="Select port" />
          </div>
          <div class="field">
            <label>Cruise</label>
            <input v-model="searchForm.ship" placeholder="Select ship" />
          </div>
          <div class="field">
            <label>Date</label>
            <input type="month" v-model="searchForm.date" />
          </div>
        </div>
        <button class="search-btn" @click="searchTrip">Search ALL</button>
      </div>

      <!-- 搜索结果 -->
      <div v-if="activeMenu === 'Search For Trip'" class="search-results">
        <h2 class="section-title">Search Results</h2>
        <div v-if="dataStore.searchResults.length > 0">
          <!-- 假设搜索结果 -->
          <div v-for="trip in dataStore.searchResults" :key="trip.id" class="result-card">
            <div class="image-container">
              <img :src="trip.image" alt="Cruise Image" />
            </div>
            <div class="info">
              <h3>{{ trip.nights }} NIGHT</h3>
              <h2>{{ trip.title }}</h2>
              <p><strong>From:</strong> {{ trip.roundTripFrom }}</p>
              <p><strong>Visiting:</strong> {{ trip.visiting }}</p>
              <p><strong>Date:</strong> {{ trip.date }}</p>
              <p>{{ trip.description }}</p>
            </div>
            <div class="price-section">
              <h2>{{ trip.price }} DH</h2>
              <p class="avg-per-person">AVG PER PERSON</p>
              <button class="reserve-btn">reserve</button>
              <p class="fees">*Taxes, fees and port expenses {{ trip.fees }} DH*</p>
            </div>
          </div>
        </div>
        <div v-else>
          <p>No results found or please search above.</p>
        </div>
      </div>


      <!-- Personal Info -->
      <div v-if="activeMenu === 'Personal Info'" class="card">
        <h2 class="section-title">Passenger Information</h2>
        <div v-if="dataStore.passenger">
          <p><strong>Name:</strong> {{ dataStore.passenger.name }}</p>
          <p><strong>Email:</strong> {{ dataStore.passenger.email }}</p>
          <p><strong>Phone:</strong> {{ dataStore.passenger.phone }}</p>
          <h3>Address</h3>
          <div v-if="dataStore.address">
            <p><strong>Street:</strong> {{ dataStore.address.street }}</p>
            <p><strong>City:</strong> {{ dataStore.address.city }}</p>
            <p><strong>State:</strong> {{ dataStore.address.state_province }}</p>
            <p><strong>Postal Code:</strong> {{ dataStore.address.postal_code }}</p>
            <p><strong>Country:</strong> {{ dataStore.address.country }}</p>
          </div>
          <button class="btn edit-btn" @click="showEditModal = true">Edit Info</button>
        </div>
        <div v-else>
          <p>Loading passenger information...</p>
        </div>
      </div>

      <!-- Group Member -->
      <div v-if="activeMenu === 'Group Member'" class="card">
        <h2 class="section-title">Group Information</h2>
        <div v-if="dataStore.group">
          <h3>Stateroom Booking</h3>
          <ul class="list">
            <li v-for="booking in dataStore.stateroomBooking" :key="booking.bookingId" class="list-item">
              <p><strong>Booking ID:</strong> {{ booking.bookingId }}</p>
              <p><strong>Room Number:</strong> {{ booking.roomNumber }}</p>
              <p><strong>Price:</strong> ${{ booking.price }}</p>
            </li>
          </ul>

          <h3>Payments</h3>
          <ul class="list">
            <li v-for="payment in dataStore.payment" :key="payment.paymentId" class="list-item">
              <p><strong>Payment ID:</strong> {{ payment.paymentId }}</p>
              <p><strong>Amount:</strong> ${{ payment.amount }}</p>
              <p><strong>Date:</strong> {{ payment.date }}</p>
              <button class="btn" @click="fetchInvoice(payment.paymentId)">View Invoice</button>
              <div v-if="dataStore.invoices[payment.paymentId]" class="invoice-box">
                <h4>Invoice Details</h4>
                <p><strong>Invoice ID:</strong> {{ dataStore.invoices[payment.paymentId].invoiceId }}</p>
                <p><strong>Billing Date:</strong> {{ dataStore.invoices[payment.paymentId].billingDate }}</p>
                <p><strong>Amount Due:</strong> ${{ dataStore.invoices[payment.paymentId].amountDue }}</p>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>Loading group information...</p>
        </div>
      </div>

      <!-- View My Trip -->
      <div v-if="activeMenu === 'View My Trip'" class="card">
        <h2 class="section-title">Trip Information</h2>
        <div v-if="dataStore.trip">
          <h3>Restaurants</h3>
          <ul class="list">
            <li v-for="restaurant in dataStore.restaurant" :key="restaurant.restaurantId" class="list-item">
              <p><strong>Name:</strong> {{ restaurant.name }}</p>
              <p><strong>Serve Type:</strong> {{ restaurant.serveType }}</p>
              <p><strong>Open:</strong> {{ restaurant.openingTime }} - {{ restaurant.closingTime }}</p>
            </li>
          </ul>

          <h3>Entertainment</h3>
          <ul class="list">
            <li v-for="entertainment in dataStore.entertainment" :key="entertainment.entertainId" class="list-item">
              <p><strong>Name:</strong> {{ entertainment.name }}</p>
              <p><strong>Units:</strong> {{ entertainment.units }}</p>
              <p><strong>Floor:</strong> {{ entertainment.floor }}</p>
            </li>
          </ul>

          <h3>Ports (Itinerary)</h3>
          <ul class="list">
            <li v-for="port in dataStore.port" :key="port.portId" class="list-item">
              <p><strong>Port Name:</strong> {{ port.name }}</p>
              <p><strong>Nearest Airport:</strong> {{ port.nearestAirport }}</p>
              <p><strong>Parking Spots:</strong> {{ port.numParkingSpots }}</p>
              <h4>Itinerary</h4>
              <ul>
                <li v-for="itinerary in port.itineraries" :key="itinerary.itineraryId">
                  <p><strong>Arrival:</strong> {{ itinerary.arrivalDateTime }}</p>
                  <p><strong>Departure:</strong> {{ itinerary.leavingDateTime }}</p>
                </li>
              </ul>
            </li>
          </ul>

          <h3>Staterooms</h3>
          <ul class="list">
            <li v-for="stateroom in dataStore.stateroom" :key="stateroom.stateroomId" class="list-item">
              <p><strong>Room Number:</strong> {{ stateroom.roomNumber }}</p>
              <p><strong>Size:</strong> {{ stateroom.sizeSqft }} sqft</p>
              <p><strong>Bathrooms:</strong> {{ stateroom.numBathroom }}</p>
              <p><strong>Beds:</strong> {{ stateroom.numBed }}</p>
              <button class="btn" @click="fetchStateroomPrice(stateroom.stateroomId)">View Price</button>
              <div v-if="dataStore.stateroomPrices[stateroom.stateroomId]" class="price-box">
                <h4>Price Details</h4>
                <p><strong>Price Per Night:</strong> ${{ dataStore.stateroomPrices[stateroom.stateroomId].pricePerNight }}</p>
                <p><strong>Vacancy:</strong> {{ dataStore.stateroomPrices[stateroom.stateroomId].isVacant ? 'Vacant' : 'Occupied' }}</p>
                <button class="btn book-btn" @click="openBookingModal(stateroom)">Book This Room</button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>Loading trip information...</p>
        </div>
      </div>

      <!-- Package Service -->
      <div v-if="activeMenu === 'Package Service'" class="card">
        <h2 class="section-title">Package Information</h2>
        <div v-if="dataStore.packages.length > 0">
          <ul class="list">
            <li v-for="pkg in dataStore.packages" :key="pkg.packageId" class="list-item">
              <p><strong>Package Name:</strong> {{ pkg.name }}</p>
              <p><strong>Charge Type:</strong> {{ pkg.chargeType }}</p>
              <p><strong>Price:</strong> ${{ pkg.price }}</p>
              <button class="btn" @click="openPurchaseModal(pkg)">Purchase</button>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>Loading package information...</p>
        </div>
      </div>
    </div>

    <!-- 编辑个人信息 Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal=false">
      <div class="modal">
        <h3>Edit Personal Information</h3>
        <label>Phone:</label>
        <input v-model="editForm.phone" type="text" />
        <label>Street:</label>
        <input v-model="editForm.street" type="text" />
        <label>City:</label>
        <input v-model="editForm.city" type="text" />
        <label>State/Province:</label>
        <input v-model="editForm.state_province" type="text" />
        <label>Postal Code:</label>
        <input v-model="editForm.postal_code" type="text" />
        <label>Country:</label>
        <input v-model="editForm.country" type="text" />

        <div class="modal-buttons">
          <button class="btn save-btn" @click="updatePersonalInfo">Save</button>
          <button class="btn cancel-btn" @click="showEditModal=false">Cancel</button>
        </div>
      </div>
    </div>

    <!-- 预订房间 Modal -->
    <div v-if="showBookingModal" class="modal-overlay" @click.self="showBookingModal=false">
      <div class="modal">
        <h3>Book Stateroom</h3>
        <label>Start Date:</label>
        <input type="date" v-model="bookingForm.startDate" />
        <label>End Date:</label>
        <input type="date" v-model="bookingForm.endDate" />
        <div class="modal-buttons">
          <button class="btn save-btn" @click="bookStateroom">Book</button>
          <button class="btn cancel-btn" @click="showBookingModal=false">Cancel</button>
        </div>
      </div>
    </div>

    <!-- 购买Package Modal -->
    <div v-if="showPurchaseModal" class="modal-overlay" @click.self="showPurchaseModal=false">
      <div class="modal">
        <h3>Purchase Package</h3>
        <p>Package: {{ selectedPackage?.name }}</p>
        <p>Price: ${{ selectedPackage?.price }}</p>
        <div class="modal-buttons">
          <button class="btn save-btn" @click="purchasePackage">Purchase</button>
          <button class="btn cancel-btn" @click="showPurchaseModal=false">Cancel</button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  height: 100vh;
  font-family: 'Roboto', sans-serif;
  background: linear-gradient(to bottom, #e0f7ff, #ffffff);
}

/* 侧边栏样式 */
.sidebar {
  width: 250px;
  background: #fff;
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  z-index: 1;
}

.sidebar-header {
  font-size: 20px;
  margin-bottom: 20px;
  color: #007acc;
  text-align: center;
}

.menu {
  list-style: none;
  padding: 0;
}

.menu li {
  padding: 12px;
  margin-bottom: 10px;
  background: #f9f9f9;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-align: center;
  font-weight: 500;
  color: #333;
}

.menu li:hover {
  background-color: #e0f7ff;
}

.menu li.active {
  background-color: #007acc;
  color: white;
}

/* 内容区域 */
.content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

/* 搜索栏样式 */
.search-bar {
  background: #f7faff;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-end;
  gap: 20px;
}

.search-fields {
  display: flex;
  gap: 20px;
  flex: 1;
}

.field {
  display: flex;
  flex-direction: column;
}

.field label {
  font-weight: 500;
  margin-bottom: 5px;
  color: #333;
}

.field input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius:5px;
}

.search-btn {
  background: #007acc;
  color:#fff;
  border:none;
  padding:10px 20px;
  border-radius:20px;
  cursor:pointer;
  transition: background 0.3s;
}

.search-btn:hover {
  background: #005f99;
}

/* 搜索结果样式 */
.search-results .result-card {
  display: flex;
  background: #fff;
  border-radius:10px;
  padding:20px;
  box-shadow:0 1px 5px rgba(0,0,0,0.1);
  margin-bottom:20px;
  gap:20px;
}

.image-container img {
  width:200px;
  height:auto;
  border-radius:10px;
  object-fit:cover;
}

.info {
  flex: 1;
}

.info h3 {
  color:#007acc;
  font-size:18px;
  margin-bottom:10px;
}

.info h2 {
  font-size:24px;
  margin-bottom:10px;
  color:#002244;
}

.price-section {
  text-align:right;
  min-width:150px;
}

.price-section h2 {
  font-size:24px;
  color:#002244;
  margin-bottom:5px;
}

.price-section .avg-per-person {
  color:#007acc;
  font-size:14px;
  margin-bottom:15px;
}

.reserve-btn {
  background:#fff;
  border:1px solid #007acc;
  color:#007acc;
  border-radius:20px;
  padding:8px 15px;
  cursor:pointer;
}

.reserve-btn:hover {
  background:#007acc;
  color:#fff;
}

.fees {
  font-size:12px;
  color:#666;
  margin-top:10px;
}

/* 卡片 */
.card {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(5px);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.section-title {
  color: #007acc;
  margin-bottom: 20px;
}

/* 列表 */
.list {
  list-style: none;
  padding: 0;
}

.list-item {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 10px;
  padding: 15px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.1);
}

/* 按钮样式 */
.btn {
  padding: 8px 15px;
  font-size: 14px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 10px;
  margin-right: 10px;
  color: #fff;
  background: #007acc;
}

.btn:hover {
  background: #005f99;
}

/* 特殊按钮 */
.edit-btn {
  background: linear-gradient(135deg, #28a745, #5cd75c);
}

.edit-btn:hover {
  background: linear-gradient(135deg, #218838, #4ec94e);
}

.book-btn {
  background: linear-gradient(135deg, #ff9900, #ffcc00);
  color: #fff;
}

.book-btn:hover {
  background: linear-gradient(135deg, #e68a00, #e6b800);
}

/* Invoice和Price等信息卡片 */
.invoice-box, .price-box {
  background: #f0f9ff;
  padding: 10px;
  border-radius: 8px;
  margin-top: 10px;
}

/* Modal样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left:0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  background: #fff;
  padding: 20px;
  border-radius:10px;
  box-shadow:0 2px 10px rgba(0,0,0,0.3);
  min-width: 300px;
}

.modal h3 {
  margin-bottom: 15px;
  color: #007acc;
}

.modal label {
  display:block;
  margin-top:10px;
  font-weight:bold;
  color:#333;
}

.modal input {
  width:100%;
  padding:8px;
  margin-top:5px;
  border:1px solid #ddd;
  border-radius:5px;
}

.modal-buttons {
  margin-top:20px;
  text-align:right;
}

.save-btn {
  background: linear-gradient(135deg, #28a745, #5cd75c);
}

.save-btn:hover {
  background: linear-gradient(135deg, #218838, #4ec94e);
}

.cancel-btn {
  background: #ff4d4f;
  margin-right:10px;
}

.cancel-btn:hover {
  background: #cc0000;
}
</style>

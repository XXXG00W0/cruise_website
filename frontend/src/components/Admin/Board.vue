<script setup>
import { ref, onMounted } from 'vue'
// 引入组件
import PassengerManage from './PassengerManage.vue'
import RoomManage from './RoomManage.vue'
import TripManage from './TripManage.vue'
import Statistic from './Statistic.vue'

const activeMenu = ref('dashboard') // 默认显示 Dashboard

const adminInfo = ref({
  name: 'Admin User',
  email: 'admin@cruiseline.com'
})

function switchMenu(menu) {
  activeMenu.value = menu
}

onMounted(() => {
  console.log('Admin page loaded')
})
</script>

<template>
  <div class="admin-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <h3 class="sidebar-header">Admin Menu</h3>
      <ul class="menu">
        <li
          v-for="menu in ['dashboard', 'Statistic','ManagePassengers', 'ManageTrips', 'ManageRooms']"
          :key="menu"
          :class="{ active: activeMenu === menu }"
          @click="switchMenu(menu)"
        >
          {{ menu.charAt(0).toUpperCase() + menu.slice(1).replace(/([A-Z])/g, ' $1') }}
        </li>
      </ul>
    </aside>

    <!-- 主内容区 -->
    <main class="content">
      <!-- Dashboard -->
      <div v-if="activeMenu === 'dashboard'" class="dashboard">
        <h2 class="dashboard-title">Welcome, {{ adminInfo.name }}</h2>
        <p class="dashboard-info">Below are some important notes and guidelines for managing the system:</p>

        <div class="note-cards">
          <div class="note-card">
            <h3>Keep Data Secure</h3>
            <p>
              Always ensure that sensitive passenger information is kept confidential.
              Update security patches and monitor logs for suspicious activities.
            </p>
          </div>

          <div class="note-card">
            <h3>Regular Backups</h3>
            <p>
              Perform regular backups of the database and files to prevent data loss. 
              Store backups offsite for extra redundancy.
            </p>
          </div>

          <div class="note-card">
            <h3>Monitor Capacity</h3>
            <p>
              Keep track of trip bookings and stateroom availability. 
              Ensure there are enough vacancies to meet demand and adjust prices accordingly.
            </p>
          </div>

          <div class="note-card">
            <h3>Maintain Data Accuracy</h3>
            <p>
              Verify that all trip, passenger, and booking data is accurate. 
              Incorrect or outdated information can lead to customer dissatisfaction.
            </p>
          </div>
        </div>
      </div>

      <!-- Statistic -->
      <div v-if="activeMenu === 'Statistic'">
        <Statistic/> 
      </div>

      <!-- Manage passengers -->
      <div v-if="activeMenu === 'ManagePassengers'">
        <PassengerManage /> 
      </div>

      <!-- Manage Trips -->
      <div v-if="activeMenu === 'ManageTrips'">
        <TripManage />
      </div>

      <!-- Manage Rooms -->
      <div v-if="activeMenu === 'ManageRooms'">
        <RoomManage /> 
      </div>
    </main>
  </div>
</template>

<style scoped>
body {
  margin: 0;
  font-family: 'Roboto', sans-serif;
  background: #f0f2f5;
}

.admin-container {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
}

.sidebar {
  width: 250px;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  font-size: 20px;
  margin-bottom: 20px;
  color: #007acc;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  padding: 12px 15px;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.menu li:hover {
  background-color: #e8f4fd;
}

.menu li.active {
  background-color: #007acc;
  color: white;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #f0f2f5;
}

.dashboard {
  max-width: 900px;
  margin: 0 auto;
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.dashboard-title {
  font-size: 24px;
  font-weight: bold;
  color: #007acc;
  margin-bottom: 10px;
}

.dashboard-subtitle {
  color: #666;
  margin-bottom: 20px;
}

.dashboard-info {
  color: #333;
  margin-bottom: 30px;
  font-size: 14px;
}

.note-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.note-card {
  background: linear-gradient(135deg, #9c6fcb, #5c6ac4);
  color: #fff;
  border-radius: 10px;
  padding: 20px;
  flex: 1 1 calc(50% - 20px);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  min-width: 200px;
}

.note-card h3 {
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: bold;
}

.note-card p {
  font-size: 14px;
  line-height: 1.5;
}

@media(max-width: 600px) {
  .note-card {
    flex: 1 1 100%;
  }
}
</style>

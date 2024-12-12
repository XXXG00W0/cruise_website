<script setup>
import { ref, onMounted } from 'vue'
// 引入 Passenger Management 组件
import PassengerManage from './PassengerManage.vue'
import RoomManage from './RoomManage.vue'
import TripManage from './TripManage.vue';
import Statistic from './Statistic.vue';

// 当前选中的菜单项
const activeMenu = ref('dashboard') // 默认显示 Dashboard

// 模拟一些数据
const adminInfo = ref({
  name: 'Admin User',
  email: 'admin@cruiseline.com'
})

// 切换菜单项
function switchMenu(menu) {
  activeMenu.value = menu
}

// 页面加载时可以初始化一些数据
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
      <div v-if="activeMenu === 'dashboard'">
        <h2>Admin Dashboard</h2>
        <p>Welcome, {{ adminInfo.name }}</p>
        <p>Email: {{ adminInfo.email }}</p>
        <p>Here you can view an overview of the system.</p>
      </div>

      <!-- Manage passengers -->
      <div v-if="activeMenu === 'Statistic'">
        <Statistic/> <!-- 引入 Passenger Management   功能 -->
      </div>


      <!-- Manage passengers -->
      <div v-if="activeMenu === 'ManagePassengers'">
        <PassengerManage /> <!-- 引入 Passenger Management 功能 -->
      </div>

      <!-- Manage Trips -->
      <div v-if="activeMenu === 'ManageTrips'">
        <TripManage /> <!-- 引入 Passenger Management 功能 -->
      </div>
      <!-- Manage Rooms -->
      <div v-if="activeMenu === 'ManageRooms'">
        <RoomManage /> 
      </div>
    </main>
  </div>
</template>

<style scoped>
.admin-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #f4f4f4;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  font-size: 20px;
  margin-bottom: 20px;
  color: #007acc;
}

.menu {
  list-style: none;
  padding: 0;
}

.menu li {
  padding: 10px 15px;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.menu li:hover {
  background-color: #eaeaea;
}

.menu li.active {
  background-color: #007acc;
  color: white;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>

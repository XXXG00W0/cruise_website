<template>
  <div class="main-container">
    <h2 class="header">Welcome to Cruise Management System</h2>
    <div class="grid-container">
      <!-- Trip -->
      <div class="card" @click="goTo('/Main/Trip')">
        <img class="card-image" src="..\..\assets\img\Trip.png" alt="Trip Image" />
        <h3 class="card-title">Trip</h3>
        <p class="card-desc">Find and explore your cruise trips.</p>
        <button class="btn" @click="goTo('/Main/Trip')">View Trips</button>
      </div>

      <!-- Self -->
      <div class="card" @click="goTo('/Main/Self')">
        <img class="card-image" src="..\..\assets\img\Self.png" alt="Profile Image" />
        <h3 class="card-title">My Profile</h3>
        <p class="card-desc">View and update your personal info.</p>
        <button class="btn" @click="goTo('/Main/Self')">My Profile</button>
      </div>

      <!-- MyTrip -->
      <div class="card" @click="goTo('/Main/MyTrip')">
        <img class="card-image" src="..\..\assets\img\MyTrip.png" alt="My Trips Image" />
        <h3 class="card-title">My Trips</h3>
        <p class="card-desc">Check out your booked rooms and trips.</p>
        <button class="btn" @click="goTo('/Main/MyTrip')">My Booked Trips</button>
      </div>

      <!-- Package -->
      <div class="card" @click="goTo('/Main/Package')">
        <img class="card-image" src="..\..\assets\img\pack.png" alt="Package Image" />
        <h3 class="card-title">Packages</h3>
        <p class="card-desc">Browse and purchase available packages.</p>
        <button class="btn" @click="goTo('/Main/Package')">View Packages</button>
      </div>

      <!-- Restraunt -->
      <div class="card" @click="goTo('/Main/Restraunt')">
        <img class="card-image" src="..\..\assets\img\Rest.png" alt="Restaurant Image" />
        <h3 class="card-title">Restaurants</h3>
        <p class="card-desc">Check out onboard dining options.</p>
        <button class="btn" @click="goTo('/Main/Restraunt')">View Restaurants</button>
      </div>

      <!-- Entertainment -->
      <div class="card" @click="goTo('/Main/Entertainment')">
        <img class="card-image" src="..\..\assets\img\Enter.png" alt="Entertainment Image" />
        <h3 class="card-title">Entertainment</h3>
        <p class="card-desc">Discover fun and activities onboard.</p>
        <button class="btn" @click="goTo('/Main/Entertainment')">View Entertainment</button>
      </div>
    </div>

    <!-- 子路由显示区 -->
    <div class="router-view-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'Main',
  setup() {
    const router = useRouter()

    function goTo(path) {
      // 阻止事件冒泡不再必须，如需仅在按钮点击才跳转，可在上层修改逻辑
      router.push(path)
    }

    return { goTo }
  }
}
</script>

<style scoped>
.main-container {
  width: 100vw;
  min-height: 100vh;
  background: linear-gradient(to bottom, #e0f7ff, #ffffff);
  font-family: 'Roboto', sans-serif;
  padding: 50px 30px;
  box-sizing: border-box;
}

.header {
  color: #007acc;
  font-size: 28px;
  margin-bottom: 40px;
  font-weight: bold;
  text-align: center;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 30px;
  padding: 0 20px;
}

.card {
  background: #fff;
  border-radius: 10px;
  box-shadow:0 2px 10px rgba(0,0,0,0.1);
  padding:20px;
  display:flex;
  flex-direction:column;
  align-items:center;
  text-align:center;
  cursor:pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow:0 4px 15px rgba(0,0,0,0.15);
}

.card-image {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 15px;
}

.card-title {
  font-size:20px;
  color:#007acc;
  margin-bottom:10px;
  font-weight:bold;
}

.card-desc {
  font-size:14px;
  color:#333;
  margin-bottom:20px;
}

.btn {
  padding:10px 20px;
  font-size:14px;
  background:#007acc;
  color:#fff;
  border:none;
  border-radius:20px;
  cursor:pointer;
  transition: background 0.3s;
}

.btn:hover {
  background:#005f99;
}

.router-view-container {
  margin-top:50px;
  background: #fff;
  border-radius:10px;
  box-shadow:0 2px 10px rgba(0,0,0,0.1);
  padding:20px;
  min-height:200px;
  box-sizing:border-box;
}
</style>

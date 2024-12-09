<template>
  <div class="restaurant-container">
    <h2 class="header">Available Restaurants</h2>

    <div v-if="isLoading" class="loading">Loading restaurants...</div>
    <div v-else-if="restaurants.length === 0">
      <el-empty description="No restaurant information available"></el-empty>
    </div>
    <div v-else class="restaurant-table">
      <table>
        <thead>
          <tr>
            <th>Restaurant Name</th>
            <th>Serve Type</th>
            <th>Opening Time</th>
            <th>Closing Time</th>
            <th>Floor</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="restaurant in restaurants" :key="restaurant.restaurant_id">
            <td>{{ restaurant.restaurant_name }}</td>
            <td>{{ restaurant.serve_type }}</td>
            <td>{{ restaurant.opening_time }}</td>
            <td>{{ restaurant.closing_time }}</td>
            <td>{{ restaurant.at_floor }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import request from '../../utils/request'

export default {
  name: 'Restaurant',
  setup() {
    const restaurants = ref([]) // 存储餐厅信息
    const isLoading = ref(false) // 加载状态

    onMounted(() => {
      fetchRestaurants() // 页面加载时获取数据
    })

    async function fetchRestaurants() {
      isLoading.value = true
      try {
        const response = await request.get('/api/Passenger/Restaurant')
        isLoading.value = false

        // 遍历解析数据并推送到 restaurants 列表
        restaurants.value = response.map(restaurant => ({
          restaurant_id: restaurant.restaurant_id,
          restaurant_name: restaurant.restaurant_name,
          serve_type: restaurant.serve_type,
          opening_time: restaurant.opening_time,
          closing_time: restaurant.closing_time,
          at_floor: restaurant.at_floor,
        }))
      } catch (err) {
        isLoading.value = false
        console.error('Error fetching restaurant information:', err)
        alert('Error fetching restaurant information');
      }
    }

    function formatDateTime(dateTimeStr) {
      if (!dateTimeStr) return ''
      const date = new Date(dateTimeStr)
      return date.toLocaleString()
    }

    return {
      restaurants,
      isLoading,
      formatDateTime,
    }
  }
}
</script>

<style scoped>
.restaurant-container {
  width: 800px;
  margin: 50px auto;
  font-family: 'Roboto', sans-serif;
}

.header {
  color: #007acc;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
  text-align: center;
}

.loading {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin: 20px 0;
}

.restaurant-table {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

thead {
  background: #007acc;
  color: #fff;
}

thead th {
  padding: 10px;
}

tbody tr {
  border-bottom: 1px solid #ddd;
}

tbody td {
  padding: 10px;
}

tbody tr:nth-child(even) {
  background: #f9f9f9;
}
</style>

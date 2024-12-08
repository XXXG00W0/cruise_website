<template>
    <div class="Restaurant-container">
      <h2 class="header">Restaurants</h2>
  
      <div v-if="isLoading" class="loading">Loading Restaurant information...</div>
      <div v-else-if="Restaurants.length === 0">
        <el-empty description="No Restaurant information available"></el-empty>
      </div>
      <div v-else class="Restaurant-list">
        <ul>
          <li v-for="Restaurant in Restaurants" :key="Restaurant.Restaurant_id" class="Restaurant-item">
            <h3>{{ Restaurant.Restaurant_name }}</h3>
            <p><strong>Serve Type:</strong> {{ Restaurant.serve_type }}</p>
            <p><strong>Opening Time:</strong> {{ formatDateTime(Restaurant.opening_time) }}</p>
            <p><strong>Closing Time:</strong> {{ formatDateTime(Restaurant.closing_time) }}</p>
            <p><strong>Floor:</strong> {{ Restaurant.at_floor }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import request from '../../utils/request'
  
  export default {
    name: 'Restaurant',
    setup() {
      const Restaurants = ref([])
      const isLoading = ref(false)
  
      onMounted(() => {
        fetchRestaurants()
      })
  
      async function fetchRestaurants() {
        isLoading.value = true
        try {
          const response = await request.get('/api/Restaurants')
          isLoading.value = false
          if (response.code === 200) {
            Restaurants.value = response.data.Restaurants
          } else {
            alert(response.message || 'Failed to fetch Restaurant information')
          }
        } catch (err) {
          console.error(err)
          alert('Error fetching Restaurant information')
          isLoading.value = false
        }
      }
  
      function formatDateTime(dtStr) {
        if (!dtStr) return ''
        const date = new Date(dtStr)
        return date.toLocaleString()
      }
  
      return {
        Restaurants,
        isLoading,
        formatDateTime
      }
    }
  }
  </script>
  
  <style scoped>
  .Restaurant-container {
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
    text-align:center;
    color:#666;
    font-size:14px;
    margin:20px 0;
  }
  
  .Restaurant-list {
    background:#fff;
    padding:20px;
    border-radius:10px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
  }
  
  .Restaurant-list ul {
    list-style:none;
    padding:0;
  }
  
  .Restaurant-item {
    background:#f9f9f9;
    padding:15px;
    border-radius:5px;
    margin-bottom:10px;
  }
  
  .Restaurant-item h3 {
    color:#007acc;
    margin-bottom:10px;
  }
  
  .Restaurant-item p {
    margin:5px 0;
  }
  </style>
  
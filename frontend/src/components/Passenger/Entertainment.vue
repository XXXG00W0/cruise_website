<template>
    <div class="entertainment-container">
      <h2 class="header">Entertainment</h2>
  
      <div v-if="isLoading" class="loading">Loading entertainment information...</div>
      <div v-else-if="entertainments.length === 0">
        <el-empty description="No entertainment information available"></el-empty>
      </div>
      <div v-else class="entertainment-list">
        <ul>
          <li v-for="ent in entertainments" :key="ent.entertain_id" class="entertainment-item">
            <h3>{{ ent.entertain_name }}</h3>
            <p><strong>Number of Units:</strong> {{ ent.num_units }}</p>
            <p><strong>Floor:</strong> {{ ent.at_floor }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import request from '../../utils/request'
  
  export default {
    name: 'Entertainment',
    setup() {
      const entertainments = ref([])
      const isLoading = ref(false)
  
      onMounted(() => {
        fetchEntertainment()
      })
  
      async function fetchEntertainment() {
        isLoading.value = true
        try {
          const response = await request.get('/api/entertainment')
          isLoading.value = false
          if (response.code === 200) {
            entertainments.value = response.data.entertainment
          } else {
            alert(response.message || 'Failed to fetch entertainment information')
          }
        } catch (err) {
          console.error(err)
          alert('Error fetching entertainment information')
          isLoading.value = false
        }
      }
  
      return {
        entertainments,
        isLoading
      }
    }
  }
  </script>
  
  <style scoped>
  .entertainment-container {
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
  
  .entertainment-list {
    background:#fff;
    padding:20px;
    border-radius:10px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
  }
  
  .entertainment-list ul {
    list-style:none;
    padding:0;
  }
  
  .entertainment-item {
    background:#f9f9f9;
    padding:15px;
    border-radius:5px;
    margin-bottom:10px;
  }
  
  .entertainment-item h3 {
    color:#007acc;
    margin-bottom:10px;
  }
  
  .entertainment-item p {
    margin:5px 0;
  }
  </style>
  
<template>
  <div class="trip-container">
    <h2 class="header">Trip Search</h2>
    <div class="search-section">
      <div class="field">
        <label>Start Date:</label>
        <input type="date" v-model="searchForm.startDate" />
      </div>
      <div class="field">
        <label>End Date:</label>
        <input type="date" v-model="searchForm.endDate" />
      </div>
      <button class="btn search-btn" @click="searchTrip">Search</button>
    </div>

    <div v-if="isLoading" class="loading">Loading trips...</div>
    <div v-else-if="trips.length === 0 && hasSearched">
      <p>No trips found for the selected date range.</p>
    </div>
    <div v-else class="trip-list">
      <h3 v-if="hasSearched">Search Results:</h3>
      <ul>
        <li v-for="trip in trips" :key="trip.trip_id" class="trip-item">
          <p><strong>Trip ID:</strong> {{ trip.trip_id }}</p>
          <p><strong>Start Date:</strong> {{ formatDate(trip.start_date) }}</p>
          <p><strong>End Date:</strong> {{ formatDate(trip.end_date) }}</p>
          <p><strong>Start Port:</strong>{{ trip.start_port_name }}</p>
          <p><strong>End Port:</strong>{{ trip.end_port_name }}</p>
          <!-- 将原来的 viewTripDetail 按钮替换为 viewTripRoomDetail -->
          <button class="btn detail-btn" @click="viewTripRoomDetail(trip.trip_id)">View Details</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import request from '../../utils/request'
import { useRouter } from 'vue-router'

export default {
  name: 'Trip',
  setup() {
    const router = useRouter()

    const searchForm = reactive({
      startDate: '',
      endDate: ''
    })

    const trips = ref([])
    const isLoading = ref(false)
    const hasSearched = ref(false)

    async function searchTrip() {
      if (!searchForm.startDate || !searchForm.endDate) {
        alert('Please select both start and end date.')
        return
      }
      isLoading.value = true
      hasSearched.value = true
      trips.value = []
      try {
        const response = await request.get('/api/Passenger/Trip', {
          params: {
            start_date: searchForm.startDate,
            end_date: searchForm.endDate
          }
        })
        isLoading.value = false
        trips.value = response
        console.log(response)
      } catch (err) {
        isLoading.value = false
        console.error(err)
        alert('Error fetching trips')
      }
    }

    // 合并逻辑的函数：直接跳转到 RoomDetail.vue 并传入 trip_id
    function viewTripRoomDetail(trip_id) {
      router.push({ path: '/Main/RoomDetail', query: { trip_id } })
    }

    function formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString()
    }

    function formatDateTime(dtStr) {
      if (!dtStr) return ''
      const date = new Date(dtStr)
      return date.toLocaleString()
    }

    return {
      searchForm,
      trips,
      isLoading,
      hasSearched,
      searchTrip,
      viewTripRoomDetail,
      formatDate,
      formatDateTime
    }
  }
}
</script>

  <style scoped>
  .trip-container {
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
  
  .search-section {
    background: #f7faff;
    padding:20px;
    border-radius:10px;
    margin-bottom:30px;
    display: flex;
    align-items: flex-end;
    gap:20px;
  }
  
  .field {
    display:flex;
    flex-direction:column;
  }
  
  .field label {
    font-weight:500;
    margin-bottom:5px;
  }
  
  .field input {
    padding:8px;
    border:1px solid #ddd;
    border-radius:5px;
  }
  
  .btn {
    padding:10px 20px;
    font-size:14px;
    border:none;
    border-radius:20px;
    cursor:pointer;
    transition: background 0.3s;
    background:#007acc;
    color:#fff;
  }
  
  .btn:hover {
    background:#005f99;
  }
  
  .search-btn {
    margin-bottom:5px;
  }
  
  .loading {
    text-align:center;
    color:#666;
    font-size:14px;
  }
  
  .trip-list {
    background:#fff;
    padding:20px;
    border-radius:10px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
  }
  
  .trip-list h3 {
    margin-bottom:20px;
    color:#007acc;
    font-weight:bold;
  }
  
  .trip-item {
    background:#f9f9f9;
    padding:15px;
    border-radius:5px;
    margin-bottom:10px;
  }
  
  .trip-item p {
    margin:5px 0;
  }
  
  .detail-btn {
    background:#28a745;
  }
  
  .detail-btn:hover {
    background:#218838;
  }
  
  .dialog-title {
    font-weight:bold;
    font-size:18px;
    margin:0;
  }
  
  .trip-detail-content {
    padding:20px;
  }
  
  .trip-detail-content h4 {
    font-size:16px;
    font-weight:bold;
    margin-top:20px;
    margin-bottom:10px;
  }
  
  .port-item {
    background:#f0f9ff;
    padding:10px;
    border-radius:5px;
    margin-bottom:10px;
  }
  
  .port-item p {
    margin:3px 0;
  }
  
  .buttons {
    margin-top:20px;
    text-align:right;
  }
  
  .room-btn {
    background:#ff9900;
  }
  
  .room-btn:hover {
    background:#e68a00;
  }
  
  .close-btn {
    background:#ff4d4f !important;
    color:#fff !important;
    border:none !important;
  }
  
  .close-btn:hover {
    background:#cc0000 !important;
  }
  </style>
  
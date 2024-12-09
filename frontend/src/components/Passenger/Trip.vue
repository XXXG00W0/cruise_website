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
            <button class="btn detail-btn" @click="viewTripDetail(trip.trip_id)">View Details</button>
          </li>
        </ul>
      </div>
  
      <el-dialog :show-close="false" :visible.sync="showDetailModal" width="50%">
        <div slot="title">
          <p class="dialog-title">Trip Details</p>
        </div>
        <div class="trip-detail-content">
          <h4>Trip Information</h4>
          <p><strong>Trip ID:</strong> {{ selectedTrip?.trip_id }}</p>
          <p><strong>Start Date:</strong> {{ formatDate(selectedTrip?.start_date) }}</p>
          <p><strong>End Date:</strong> {{ formatDate(selectedTrip?.end_date) }}</p>
  
          <h4>Ports (Itinerary)</h4>
          <ul v-if="selectedTrip?.ports">
            <li v-for="port in selectedTrip.ports" :key="port.port_id" class="port-item">
              <p><strong>Port Name:</strong> {{ port.port_name }}</p>
              <p><strong>Nearest Airport:</strong> {{ port.nearest_airport }}</p>
              <p><strong>Parking Spots:</strong> {{ port.num_parking_spots }}</p>
              <h5>Itineraries</h5>
              <ul>
                <li v-for="itinerary in port.itineraries" :key="itinerary.itinerary_id">
                  <p><strong>Arrival:</strong> {{ formatDateTime(itinerary.arrival_date_time) }}</p>
                  <p><strong>Departure:</strong> {{ formatDateTime(itinerary.leaving_date_time) }}</p>
                </li>
              </ul>
            </li>
          </ul>
  
          <div class="buttons">
            <button class="btn room-btn" @click="goToRoomDetail(selectedTrip.trip_id)">Go to Room Details</button>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button size="small" class="close-btn" @click="showDetailModal=false">Close</el-button>
        </span>
      </el-dialog>
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
  
      const showDetailModal = ref(false)
      const selectedTrip = ref(null)
  
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
              startDate: searchForm.startDate,
              endDate: searchForm.endDate
            }
          })
          isLoading.value = false
          if (response.code === 200) {
            trips.value = response.data.trips
          } else {
            alert(response.message || 'Failed to fetch trips')
          }
        } catch (err) {
          isLoading.value = false
          console.error(err)
          alert('Error fetching trips')
        }
      }
  
      async function viewTripDetail(tripId) {
        try {
          const response = await request.get(`/api/trip-detail/${tripId}`)
          if (response.code === 200) {
            selectedTrip.value = response.data.trip
            showDetailModal.value = true
          } else {
            alert(response.message || 'Failed to fetch trip details')
          }
        } catch (err) {
          console.error(err)
          alert('Error fetching trip details')
        }
      }
  
      function goToRoomDetail(tripId) {
        // Navigate to RoomDetail with tripId as query param or param
        // Adjust the path according to your router setup
        router.push({ path: '/Main/RoomDetail', query: { tripId } })
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
        showDetailModal,
        selectedTrip,
        searchTrip,
        viewTripDetail,
        goToRoomDetail,
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
  
<template>
  <div class="my-trip-container">
    <h2 class="header">My Booked Trips</h2>

    <div v-if="isLoading" class="loading">Loading your bookings...</div>
    <div v-else-if="!bookings || bookings.length === 0">
      <el-empty description="No bookings found"></el-empty>
    </div>
    <div v-else>
      <div v-for="(booking, index) in bookings" :key="index" class="booking-item">
        <h3>Trip ID: {{ booking.trip_id }}</h3>
        
        <div class="info-section">
          <h4>Stateroom Information:</h4>
          <!-- 由于 stateroom_information 是个数组，这里需要遍历 -->
          <div v-for="(stateroom, sIndex) in booking.stateroom_information" :key="sIndex">
            <p><strong>Room Number:</strong> {{ stateroom.room_number }}</p>
            <p><strong>Location:</strong> {{ stateroom.location }}</p>
            <p><strong>Beds:</strong> {{ stateroom.num_bed }}</p>
            <p><strong>Bathrooms:</strong> {{ stateroom.num_bathroom }}</p>
            <p><strong>Balconies:</strong> {{ stateroom.num_balcony }}</p>
            <p><strong>Size:</strong> {{ stateroom.size_sqft }} sqft</p>
            <p><strong>Stateroom Type:</strong> {{ stateroom.stateroom_type }}</p>
          </div>

          <h4>Trip Information:</h4>
          <p><strong>Trip ID:</strong> {{ booking.trip_id }}</p>
          <p><strong>Start Date:</strong> {{ booking.start_date }}</p>
          <p><strong>End Date:</strong> {{ booking.end_date }}</p>

          <h4>Ports (Itinerary):</h4>
          <!-- 根据你的返回数据结构，如果 ports 是一个数组，那么这里直接遍历 -->
          <div v-if="booking.ports && booking.ports.length > 0">
            <div v-for="(port, pIndex) in booking.ports" :key="pIndex" class="port-item">
              <p><strong>Port Name:</strong> {{ port.port_name }}</p>
              <p><strong>Arrival:</strong> {{ port.arrival_date_time }}</p>
              <p><strong>Departure:</strong> {{ port.leaving_date_time }}</p>
            </div>
          </div>
          <div v-else>
            <p>No port/itinerary information available for this trip.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import { ref, onMounted } from 'vue'
import request from '../../utils/request'

export default {
  name: 'MyTrip',
  setup() {
    const bookings = ref([])
    const isLoading = ref(false)

    onMounted(() => {
      fetchMyBookings()
    })

    async function fetchMyBookings() {
      isLoading.value = true
      try {
        const response = await request.get('/api/Passenger/MyTrip')
        isLoading.value = false
        bookings.value = response.trips
        console.log("My bookings:", bookings.value)
      } catch (err) {
        console.error(err)
        alert('Error fetching bookings')
        isLoading.value = false
      }
    }

    // 一定要return出去，否则模板无法访问这些变量
    return {
      bookings,
      isLoading
    }
  }
}
</script>
  
  <style scoped>
  .my-trip-container {
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
  
  .booking-item {
    background:#fff;
    padding:20px;
    border-radius:10px;
    box-shadow:0 1px 5px rgba(0,0,0,0.1);
    margin-bottom:20px;
  }
  
  .booking-item h3 {
    color:#007acc;
    margin-bottom:10px;
  }
  
  .info-section {
    margin-top:10px;
  }
  
  .info-section h4 {
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
  </style>
  
<template>
    <div class="my-trip-container">
      <h2 class="header">My Booked Trips</h2>
  
      <div v-if="isLoading" class="loading">Loading your bookings...</div>
      <div v-else-if="bookings.length === 0">
        <el-empty description="No bookings found"></el-empty>
      </div>
      <div v-else>
        <div v-for="(booking, index) in bookings" :key="index" class="booking-item">
          <h3>Booking ID: {{ booking.bookingId }}</h3>
          <div class="info-section">
            <h4>Stateroom Information:</h4>
            <p><strong>Room Number:</strong> {{ booking.stateroom.room_number }}</p>
            <p><strong>Location:</strong> {{ booking.stateroom.location }}</p>
            <p><strong>Beds:</strong> {{ booking.stateroom.num_bed }}</p>
            <p><strong>Bathrooms:</strong> {{ booking.stateroom.num_bathroom }}</p>
            <p><strong>Balconies:</strong> {{ booking.stateroom.num_balcony }}</p>
            <p><strong>Size:</strong> {{ booking.stateroom.size_sqft }} sqft</p>
  
            <h4>Trip Information:</h4>
            <p><strong>Trip ID:</strong> {{ booking.trip.trip_id }}</p>
            <p><strong>Start Date:</strong> {{ formatDate(booking.trip.start_date) }}</p>
            <p><strong>End Date:</strong> {{ formatDate(booking.trip.end_date) }}</p>
  
            <h4>Ports (Itinerary):</h4>
            <div v-if="booking.trip.ports && booking.trip.ports.length > 0">
              <div v-for="port in booking.trip.ports" :key="port.port_id" class="port-item">
                <p><strong>Port Name:</strong> {{ port.port_name }}</p>
                <p><strong>Nearest Airport:</strong> {{ port.nearest_airport }}</p>
                <p><strong>Parking Spots:</strong> {{ port.num_parking_spots }}</p>
                <h5>Itineraries:</h5>
                <ul>
                  <li v-for="itinerary in port.itineraries" :key="itinerary.itinerary_id">
                    <p><strong>Arrival:</strong> {{ formatDateTime(itinerary.arrival_date_time) }}</p>
                    <p><strong>Departure:</strong> {{ formatDateTime(itinerary.leaving_date_time) }}</p>
                  </li>
                </ul>
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
          const response = await request.get('/api/my-bookings')
          isLoading.value = false
          if (response.code === 200) {
            // Assume response.data.bookings is an array of booking objects
            // Each booking includes stateroom and trip info
            bookings.value = response.data.bookings
          } else {
            alert(response.message || 'Failed to fetch bookings')
          }
        } catch (err) {
          console.error(err)
          alert('Error fetching bookings')
          isLoading.value = false
        }
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
        bookings,
        isLoading,
        formatDate,
        formatDateTime
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
  
<template>
    <div class="trip-manage-container">
      <h2 class="header">Trip Management</h2>
      <p>Here you can edit the start date of trips.</p>
  
      <div v-if="isLoading" class="loading">Loading trips...</div>
      <div v-else class="table-container">
        <table class="trip-table">
          <thead>
            <tr>
              <th>Trip ID</th>
              <th>Trip Name</th>
              <th>Current Start Date</th>
              <th>End Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in trips" :key="t.trip_id">
              <td>{{ t.trip_id }}</td>
              <td>{{ t.trip_name }}</td>
              <td>{{ t.start_date }}</td>
              <td>{{ t.end_date }}</td>
              <td>
                <button @click="editTrip(t)">Edit Start Date</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Edit Trip Start Date Dialog -->
      <div v-if="showDialog" class="edit-dialog">
        <h3 class="dialog-title">Edit Trip Start Date</h3>
        <div class="dialog-content">
          <div class="field">
            <label for="edit-trip-id">Trip ID:</label>
            <input id="edit-trip-id" v-model="formData.trip_id" type="text" readonly />
          </div>
          <div class="field">
            <label for="edit-start-date">Start Date:</label>
            <input id="edit-start-date" v-model="formData.start_date" type="date" />
          </div>
        </div>
        <div class="dialog-actions">
          <button @click="saveTrip">Save</button>
          <button @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, reactive } from 'vue'
  import request from '../../utils/request'
  
  const trips = ref([])
  const isLoading = ref(false)
  const showDialog = ref(false)
  const editingTripId = ref(null)
  
  const formData = reactive({
    trip_id: '',
    start_date: ''
  })
  
  onMounted(() => {
    fetchTrips()
  })
  
  async function fetchTrips() {
    isLoading.value = true
    try {
      const response = await request.get('/api/Admin/TripManage')
      // 假设返回的数据结构中包含 trip 列表在 response.data.trips 中
      isLoading.value = false
      trips.value = response.trips || []
    } catch (err) {
      console.error(err)
      alert('Error fetching trips')
      isLoading.value = false
    }
  }
  
  function editTrip(trip) {
    editingTripId.value = trip.trip_id
    formData.trip_id = trip.trip_id
    formData.start_date = trip.start_date
    showDialog.value = true
  }
  
  async function saveTrip() {
    try {
      // 根据实际情况选择 POST 或 PATCH
      await request.post('/api/Admin/UpdateTripStartDate', {
        trip_id: formData.trip_id,
        start_date: formData.start_date
      })
      // 保存成功后刷新行程数据
      await fetchTrips()
      showDialog.value = false
    } catch (err) {
      console.error(err)
      alert('Error saving trip start date')
    }
  }
  
  function cancelEdit() {
    showDialog.value = false
    editingTripId.value = null
    formData.trip_id = ''
    formData.start_date = ''
  }
  </script>
  
  <style scoped>
  .trip-manage-container {
    font-family: 'Roboto', sans-serif;
  }
  
  .header {
    color: #007acc;
    font-size: 24px;
    margin-bottom: 20px;
    font-weight: bold;
  }
  
  .loading {
    text-align: center;
    color: #666;
    font-size: 14px;
    margin: 20px 0;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .trip-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .trip-table th, .trip-table td {
    border: 1px solid #ddd;
    padding: 8px;
    font-size: 14px;
    text-align: left;
  }
  
  .trip-table th {
    background: #f0f9ff;
    font-weight: bold;
    color: #007acc;
  }
  
  .field {
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
  }
  
  .field label {
    font-weight: 500;
    margin-bottom: 5px;
  }
  
  .field input {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
  }
  
  .dialog-title {
    font-weight: bold;
    font-size: 18px;
    margin: 0;
  }
  
  .dialog-content {
    padding: 10px 0;
  }
  
  .dialog-actions {
    display: flex;
    gap: 10px;
  }
  
  .edit-dialog {
    border: 1px solid #ddd;
    background: #fff;
    padding: 20px;
    position: absolute;
    top: 100px;
    left: 100px;
    z-index: 999;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-radius: 5px;
  }
  </style>
  
<template>
  <div class="trip-manage-container">
    <h2 class="header">Trip Management</h2>
    <p>Here you can manage trips: create new, edit or delete existing trips.</p>
  
    <div>
      <button class="add-button" @click="openCreateDialog">Add New Trip</button>
    </div>

    <div v-if="isLoading" class="loading">Loading trips...</div>
    <div v-else class="table-container">
      <table class="trip-table">
        <thead>
          <tr>
            <th>Trip ID</th>
            <th>Start Port</th>
            <th>End Port</th>
            <th>Current Start Date</th>
            <th>End Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in trips" :key="t.trip_id">
            <td>{{ t.trip_id }}</td>
            <td>{{ t.start_port_id }}</td>
            <td>{{ t.end_port_id }}</td>
            <td>{{ t.start_date }}</td>
            <td>{{ t.end_date }}</td>
            <td>
              <button @click="editTrip(t)">Edit</button>
              <button @click="deleteTrip(t.trip_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  
    <!-- Create Trip Dialog -->
    <div v-if="showCreateDialog" class="edit-dialog">
      <h3 class="dialog-title">Add New Trip</h3>
      <div class="dialog-content">
        <div class="field">
          <label for="create-start-date">Start Date:</label>
          <input id="create-start-date" v-model="createForm.start_date" type="date" />
        </div>
        <div class="field">
          <label for="create-end-date">End Date:</label>
          <input id="create-end-date" v-model="createForm.end_date" type="date" />
        </div>
        <div class="field">
          <label for="create-start-port">Start Port ID:</label>
          <input id="create-start-port" v-model="createForm.start_port_id" type="text" />
        </div>
        <div class="field">
          <label for="create-end-port">End Port ID:</label>
          <input id="create-end-port" v-model="createForm.end_port_id" type="text" />
        </div>
      </div>
      <div class="dialog-actions">
        <button @click="saveNewTrip">Save</button>
        <button @click="cancelCreate">Cancel</button>
      </div>
    </div>

    <!-- Edit Trip Start/End Date Dialog -->
    <div v-if="showEditDialog" class="edit-dialog">
      <h3 class="dialog-title">Edit Trip</h3>
      <div class="dialog-content">
        <div class="field">
          <label>Trip ID:</label>
          <input v-model="editForm.trip_id" type="text" readonly />
        </div>
        <div class="field">
          <label for="edit-start-date">Start Date:</label>
          <input id="edit-start-date" v-model="editForm.start_date" type="date" />
        </div>
        <div class="field">
          <label for="edit-end-date">End Date:</label>
          <input id="edit-end-date" v-model="editForm.end_date" type="date" />
        </div>
      </div>
      <div class="dialog-actions">
        <button @click="updateTrip">Save</button>
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

// 控制创建对话框状态
const showCreateDialog = ref(false)
const createForm = reactive({
  start_date: '',
  end_date: '',
  start_port_id: '',
  end_port_id: ''
})

// 控制编辑对话框状态
const showEditDialog = ref(false)
const editForm = reactive({
  trip_id: '',
  start_date: '',
  end_date: ''
})

onMounted(() => {
  fetchTrips()
})

async function fetchTrips() {
  isLoading.value = true
  try {
    const response = await request.get('/api/Admin/ManageTrip')
    isLoading.value = false
    trips.value = response.trips || []
  } catch (err) {
    console.error(err)
    alert('Error fetching trips')
    isLoading.value = false
  }
}

function openCreateDialog() {
  showCreateDialog.value = true
}

function cancelCreate() {
  showCreateDialog.value = false
  // 重置表单
  createForm.start_date = ''
  createForm.end_date = ''
  createForm.start_port_id = ''
  createForm.end_port_id = ''
}

async function saveNewTrip() {
  try {
    await request.post('/api/Admin/ManageTrip', {
      start_date: createForm.start_date,
      end_date: createForm.end_date,
      start_port_id: createForm.start_port_id,
      end_port_id: createForm.end_port_id
    })
    await fetchTrips()
    cancelCreate()
  } catch (err) {
    console.error(err)
    alert('Error creating trip')
  }
}

function editTrip(trip) {
  editForm.trip_id = trip.trip_id
  // 假设后端返回的 start_date / end_date 是 YYYY-MM-DD 格式，如需转换请在此处理
  editForm.start_date = trip.start_date
  editForm.end_date = trip.end_date
  showEditDialog.value = true
}

function cancelEdit() {
  showEditDialog.value = false
  editForm.trip_id = ''
  editForm.start_date = ''
  editForm.end_date = ''
}

async function updateTrip() {
  try {
    await request.put('/api/Admin/ManageTrip', {
      trip_id: editForm.trip_id,
      start_date: editForm.start_date,
      end_date: editForm.end_date
    })
    await fetchTrips()
    cancelEdit()
  } catch (err) {
    console.error(err)
    alert('Error updating trip')
  }
}

async function deleteTrip(trip_id) {
  if (confirm(`Are you sure you want to delete trip ID ${trip_id}? This action is irreversible.`)) {
    try {
      await request.delete('/api/Admin/ManageTrip', { data: { trip_id } })
      await fetchTrips()
    } catch (err) {
      console.error(err)
      alert('Error deleting trip')
    }
  }
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

.add-button {
  margin: 10px 0;
  padding: 8px 10px;
  background: #007acc;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.add-button:hover {
  background: #005fa3;
}
</style>

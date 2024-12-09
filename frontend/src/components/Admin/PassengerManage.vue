<template>
  <div class="passenger-manage-container">
    <h2 class="header">Passenger Management</h2>
    <p>Here you can add, edit, or delete passengers and view their group info.</p>

    <div class="top-actions">
      <button class="btn add-btn" @click="openAddDialog">Add Passenger</button>
    </div>

    <div v-if="isLoading" class="loading">Loading passengers...</div>
    <div v-else-if="passengers.length === 0">
      <el-empty description="No passengers found"></el-empty>
    </div>
    <div v-else class="table-container">
      <table class="passenger-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Phone</th>
            <th>Gender</th>
            <th>Nationality</th>
            <th>Group ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in passengers" :key="p.passenger_id">
            <td>{{ p.passenger_id }}</td>
            <td>{{ p.first_name }}</td>
            <td>{{ p.last_name }}</td>
            <td>{{ p.phone }}</td>
            <td>{{ p.gender }}</td>
            <td>{{ p.nationality }}</td>
            <td>{{ p.group_id }}</td>
            <td>
              <button class="btn edit-btn" @click="openEditDialog(p)">Edit</button>
              <button class="btn delete-btn" @click="deletePassenger(p.passenger_id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Dialog -->
    <el-dialog :visible.sync="showDialog" width="30%" :before-close="handleClose">
      <span slot="title">
        <p class="dialog-title">{{ editingPassengerId ? 'Edit Passenger' : 'Add Passenger' }}</p>
      </span>
      <div class="dialog-content">
        <div class="field">
          <label>First Name:</label>
          <input type="text" v-model="formData.first_name" />
        </div>
        <div class="field">
          <label>Last Name:</label>
          <input type="text" v-model="formData.last_name" />
        </div>
        <div class="field">
          <label>Email:</label>
          <input type="text" v-model="formData.last_name" />
        </div>
        <div class="field">
          <label>Phone:</label>
          <input type="text" v-model="formData.phone" />
        </div>
        <div class="field">
          <label>Gender:</label>
          <input type="text" v-model="formData.gender" />
        </div>
        <div class="field">
          <label>Nationality:</label>
          <input type="text" v-model="formData.nationality" />
        </div>
        <div class="field">
          <label>Group ID:</label>
          <input type="number" v-model.number="formData.group_id" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import request from '../../utils/request'
import { ElMessageBox } from 'element-plus'

const passengers = ref([])
const isLoading = ref(false)
const showDialog = ref(false)
const editingPassengerId = ref(null)

// 表单数据
const formData = reactive({
  first_name: '',
  last_name: '',
  phone: '',
  gender: '',
  nationality: '',
  group_id: null
})

onMounted(() => {
  fetchPassengers()
})

async function fetchPassengers() {
  isLoading.value = true
  try {
    const response = await request.get('/api/Admin/PassengerManage')
    isLoading.value = false
    if (response.code === 200) {
      // Assume response.data.passengers is an array of passenger objects:
      // Each passenger: { passenger_id, first_name, last_name, phone, gender, nationality, group_id }
      passengers.value = response.data.passengers
    } else {
      alert(response.message || 'Failed to fetch passengers')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching passengers')
    isLoading.value = false
  }
}

function openAddDialog() {
  editingPassengerId.value = null
  resetForm()
  showDialog.value = true
}

function openEditDialog(passenger) {
  editingPassengerId.value = passenger.passenger_id
  formData.first_name = passenger.first_name
  formData.last_name = passenger.last_name
  formData.phone = passenger.phone
  formData.gender = passenger.gender
  formData.nationality = passenger.nationality
  formData.group_id = passenger.group_id
  showDialog.value = true
}

function resetForm() {
  formData.first_name = ''
  formData.last_name = ''
  formData.phone = ''
  formData.gender = ''
  formData.nationality = ''
  formData.group_id = null
}

async function savePassenger() {
  if (!formData.first_name || !formData.last_name || !formData.phone || !formData.gender || !formData.nationality) {
    alert('Please fill in all required fields.')
    return
  }

  try {
    let response
    if (editingPassengerId.value) {
      // Update existing passenger
      response = await request.put(`/api/admin/manage_users/${editingPassengerId.value}`, {
        first_name: formData.first_name,
        last_name: formData.last_name,
        phone: formData.phone,
        gender: formData.gender,
        nationality: formData.nationality,
        group_id: formData.group_id
      })
    } else {
      // Add new passenger
      response = await request.post('/api/Admin/PassengerManage', {
        first_name: formData.first_name,
        last_name: formData.last_name,
        phone: formData.phone,
        gender: formData.gender,
        nationality: formData.nationality,
        group_id: formData.group_id
      })
    }

    if (response.code === 200) {
      alert(editingPassengerId.value ? 'Passenger updated successfully' : 'Passenger added successfully')
      showDialog.value = false
      fetchPassengers()
    } else {
      alert(response.message || 'Failed to save passenger')
    }
  } catch (err) {
    console.error(err)
    alert('Error saving passenger')
  }
}

async function deletePassenger(passenger_id) {
  const confirmed = await ElMessageBox.confirm('Are you sure you want to delete this passenger?', 'Warning', { type: 'warning' })
    .then(() => true)
    .catch(() => false)
  if (!confirmed) return

  try {
    const response = await request.delete(`/api/Admin/PassengerManage/${passenger_id}`)
    if (response.code === 200) {
      alert(`Passenger with ID ${passenger_id} deleted successfully.`)
      fetchPassengers()
    } else {
      alert(response.message || 'Failed to delete passenger')
    }
  } catch (err) {
    console.error(err)
    alert('Error deleting passenger')
  }
}

function handleClose() {
  showDialog.value = false
}
</script>

<style scoped>
.passenger-manage-container {
  font-family: 'Roboto', sans-serif;
}

.header {
  color: #007acc;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
}

.loading {
  text-align:center;
  color:#666;
  font-size:14px;
  margin:20px 0;
}

.top-actions {
  margin-bottom:20px;
  text-align:right;
}

.btn {
  padding:8px 15px;
  font-size:14px;
  border:none;
  border-radius:20px;
  cursor:pointer;
  transition: background 0.3s;
  margin-left:10px;
  color:#fff;
  background:#007acc;
}

.btn:hover {
  background:#005f99;
}

.add-btn {
  background:#28a745;
}

.add-btn:hover {
  background:#218838;
}

.edit-btn {
  background:#ffc107;
  color:#333;
}

.edit-btn:hover {
  background:#e6a700;
}

.delete-btn {
  background:#ff4d4f;
}

.delete-btn:hover {
  background:#cc0000;
  color:#fff;
}

.table-container {
  overflow-x:auto;
}

.passenger-table {
  width:100%;
  border-collapse:collapse;
  margin-bottom:20px;
}

.passenger-table th, .passenger-table td {
  border:1px solid #ddd;
  padding:8px;
  font-size:14px;
  text-align:left;
}

.passenger-table th {
  background:#f0f9ff;
  font-weight:bold;
  color:#007acc;
}

.field {
  margin-bottom:15px;
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
  font-size:14px;
}

.dialog-title {
  font-weight:bold;
  font-size:18px;
  margin:0;
}

.dialog-content {
  padding:10px 0;
}
</style>

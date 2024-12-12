<template>
  <div class="passenger-manage-container">
    <h2 class="header">Passenger Management</h2>
    <p>Here you can view and delete passengers.</p>

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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in passengers" :key="p.id">
            <td>{{ p.id }}</td>
            <td>{{ p.first_name }}</td>
            <td>{{ p.last_name }}</td>
            <td>{{ p.phone }}</td>
            <td>{{ p.gender }}</td>
            <td>{{ p.nationality }}</td>
            <td>
              <button class="btn delete-btn" @click="deletePassenger(p.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../utils/request'
import { ElMessageBox } from 'element-plus'

const passengers = ref([])
const isLoading = ref(false)

onMounted(() => {
  fetchPassengers()
})

async function fetchPassengers() {
  isLoading.value = true
  try {
    // 后端GET请求：/api/Admin/UserManage
    const response = await request.get('/api/Admin/UserManage')
    isLoading.value = false

    // 返回数据格式: { "passengers": [ { "id", "first_name", "last_name", "phone", "gender", "nationality" } ] }
    if (response.passengers) {
      passengers.value = response.passengers
    } else {
      alert(response.message || 'Failed to fetch passengers')
    }
  } catch (err) {
    console.error(err)
    alert('Error fetching passengers')
    isLoading.value = false
  }
}

async function deletePassenger(passenger_id) {
  const confirmed = await ElMessageBox.confirm('Are you sure you want to delete this passenger?', 'Warning', { type: 'warning' })
    .then(() => true)
    .catch(() => false)
  if (!confirmed) return

  try {
    const response = await request.delete('/api/Admin/UserManage', { data: { passenger_id } })

    if (response.message && response.message.includes('deleted successfully')) {
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

.delete-btn {
  background:#ff4d4f;
}

.delete-btn:hover {
  background:#cc0000;
  color:#fff;
}

</style>

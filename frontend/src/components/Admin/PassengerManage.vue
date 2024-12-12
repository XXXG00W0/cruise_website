<template>
  <div class="passenger-manage-container">
    <div class="card">
      <h2 class="header">Passenger Management</h2>
      <p class="sub-header">View and delete passengers easily.</p>

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
                <button class="btn delete-btn" @click="openWarningDialog(p.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 只有 showConfirmDialog 为 true 时，el-dialog 才会渲染并显示 -->
        <el-dialog
          v-if="showConfirmDialog"
          title="Warning"
          :visible.sync="showConfirmDialog"
          width="30%"
          :close-on-click-modal="false"
        >
          <span>Are you sure you want to delete this passenger?</span>
          <div slot="footer" class="dialog-footer">
            <button class="btn cancel-btn" @click="showConfirmDialog = false">Cancel</button>
            <button class="btn delete-btn" @click="confirmDelete">Confirm</button>
          </div>
        </el-dialog>

        <!-- 在表格下面展示警告信息 -->
        <div class="warning-container" v-if="showWarning">
          <span class="warning-icon">⚠</span>
          <span class="warning-text">Please be cautious when deleting passengers. This action is irreversible.</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../utils/request'

const passengers = ref([])
const isLoading = ref(false)
const showConfirmDialog = ref(false)
const selectedPassengerId = ref(null) // 存储要删除的 passenger_id
const showWarning = ref(true)

onMounted(() => {
  fetchPassengers()
})

async function fetchPassengers() {
  isLoading.value = true
  try {
    const response = await request.get('/api/Admin/UserManage')
    isLoading.value = false

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

// 打开模态框并设置 passenger_id
function openWarningDialog(passenger_id) {
  selectedPassengerId.value = passenger_id
  showConfirmDialog.value = true
}

// 确认删除操作
async function confirmDelete() {
  const passenger_id = selectedPassengerId.value
  showConfirmDialog.value = false // 关闭对话框

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
  background: #f5f8fa;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
}

.card {
  background: #fff;
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.header {
  color: #007acc;
  font-size: 24px;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center;
}

.sub-header {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 30px;
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

.passenger-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  font-size: 14px;
}

.passenger-table th,
.passenger-table td {
  padding: 12px 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
  white-space: nowrap;
}

.passenger-table th {
  background: #f0f9ff;
  font-weight: bold;
  color: #007acc;
  position: sticky;
  top: 0;
  z-index: 1;
}

.passenger-table tbody tr:nth-child(even) {
  background: #fafafa;
}

.btn {
  padding: 6px 12px;
  font-size: 13px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
  color: #fff;
  background: #007acc;
}

.btn:hover {
  background: #005f99;
}

.cancel-btn {
  background: #ccc;
}

.cancel-btn:hover {
  background: #aaa;
}

.delete-btn {
  background: #ff4d4f;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.delete-btn:hover {
  background: #cc0000;
}

.warning-container {
  display: flex;
  align-items: center;
  background: #fffbe5;
  border: 1px solid #ffe58f;
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
  font-size: 14px;
  color: #614700;
}

.warning-icon {
  font-size: 18px;
  margin-right: 8px;
}

.warning-text {
  line-height: 1.4;
}
</style>

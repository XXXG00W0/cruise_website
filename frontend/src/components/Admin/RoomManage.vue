<template>
  <div class="room-manage-container">
    <h2 class="header">Room Price Management</h2>
    <p>You can only edit the price of staterooms here.</p>

    <div v-if="isLoading" class="loading">Loading staterooms...</div>
    <div v-else class="table-container">
      <table class="room-table">
        <thead>
          <tr>
            <th>Price ID</th>
            <th>Stateroom ID</th>
            <th>Trip ID</th>
            <th>Current Price (USD)</th>
            <th>Vacant</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in rooms" :key="r.stateroom_id">
            <td>{{ r.price_id }}</td>
            <td>{{ r.stateroom_id }}</td>
            <td>{{ r.trip_id }}</td>
            <td>{{ r.price_per_night }}</td>
            <td>{{ r.is_vacant }}</td>
            <td>
              <button @click="editRoomPrice(r)">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit Price Dialog -->
    <div v-if="showDialog" class="edit-dialog">
      <h3 class="dialog-title">Edit Room Price</h3>
      <div class="dialog-content">
        <div class="field">
          <label for="edit-stateroom-id">Stateroom ID:</label>
          <input id="edit-stateroom-id" v-model="formData.stateroom_id" type="text" readonly />
        </div>
        <div class="field">
          <label for="edit-price">Price (USD):</label>
          <input id="edit-price" v-model="formData.price" type="number" min="0" />
        </div>
      </div>
      <div class="dialog-actions">
        <button @click="savePrice">Save</button>
        <button @click="cancelEdit">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import request from '../../utils/request'

const rooms = ref([])
const isLoading = ref(false)
const showDialog = ref(false)
const editingRoomId = ref(null)

// Form data for editing room price
const formData = reactive({
  stateroom_id: '',
  price: 0
})

onMounted(() => {
  fetchRooms()
})

async function fetchRooms() {
  isLoading.value = true
  try {
    const response = await request.get('/api/Admin/RoomPriceManage')
    isLoading.value = false
    rooms.value = response.stateroom_prices
  } catch (err) {
    console.error(err)
    alert('Error fetching staterooms')
    isLoading.value = false
  }
}

// 打开编辑对话框，并填充对应数据
function editRoomPrice(room) {
  editingRoomId.value = room.stateroom_id
  formData.stateroom_id = room.stateroom_id
  formData.price = room.price_per_night
  showDialog.value = true
}

// 保存修改后的价格
async function savePrice() {
  try {
    await request.post('/api/Admin/RoomPriceManage', {
      stateroom_id: formData.stateroom_id,
      price: formData.price
    })
    // 保存成功后刷新房间数据
    await fetchRooms()
    showDialog.value = false
  } catch (err) {
    console.error(err)
    alert('Error saving price')
  }
}

// 取消编辑
function cancelEdit() {
  showDialog.value = false
  editingRoomId.value = null
  formData.stateroom_id = ''
  formData.price = 0
}
</script>

<style scoped>
.room-manage-container {
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

.room-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.room-table th, .room-table td {
  border: 1px solid #ddd;
  padding: 8px;
  font-size: 14px;
  text-align: left;
}

.room-table th {
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

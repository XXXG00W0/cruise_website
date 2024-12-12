<template>
  <div class="room-manage-container">
    <div class="card">
      <h2 class="header">Room Price Management</h2>
      <p class="sub-header">Manage prices of staterooms: add, edit or delete easily.</p>

      <div class="top-actions">
        <button class="btn add-btn" @click="openAddDialog">Add New Room</button>
      </div>

      <div v-if="isLoading" class="loading">Loading stateroom prices...</div>
      <div v-else-if="rooms.length === 0">
        <el-empty description="No stateroom prices found"></el-empty>
      </div>
      <div v-else class="table-container">
        <table class="room-table">
          <thead>
            <tr>
              <th>Price ID</th>
              <th>Stateroom ID</th>
              <th>Trip ID</th>
              <th>Price (USD)</th>
              <th>Vacant</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in rooms" :key="r.price_id">
              <td>{{ r.price_id }}</td>
              <td>{{ r.stateroom_id }}</td>
              <td>{{ r.trip_id }}</td>
              <td>{{ r.price_per_night }}</td>
              <td>{{ r.is_vacant }}</td>
              <td>
                <button class="btn edit-btn" @click="openEditDialog(r)">Edit</button>
                <button class="btn delete-btn" @click="openDeleteDialog(r.price_id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add / Edit Price Dialog -->
    <el-dialog
      v-if="showDialog"
      :title="editingPriceId ? 'Edit Room Price' : 'Add New Room Price'"
      :visible.sync="showDialog"
      width="30%"
      :close-on-click-modal="false"
    >
      <div class="dialog-content">
        <!-- 如果是编辑，Price ID不可编辑，但Stateroom、Trip ID和Price可编辑。创建时都可输入 -->
        <div class="field" v-if="editingPriceId">
          <label>Price ID:</label>
          <input type="text" v-model="formData.price_id" disabled />
        </div>

        <div class="field">
          <label>Stateroom ID:</label>
          <input type="text" v-model="formData.stateroom_id" :disabled="editingPriceId"/>
        </div>

        <div class="field">
          <label>Trip ID:</label>
          <input type="text" v-model="formData.trip_id" :disabled="editingPriceId"/>
        </div>

        <div class="field">
          <label>Price (USD):</label>
          <input type="number" v-model.number="formData.price_per_night" min="0" />
        </div>

        <div class="field check-field">
          <label>Vacant:</label>
          <input type="checkbox" v-model="formData.is_vacant" />
        </div>
      </div>

      <div slot="footer" class="dialog-footer">
        <button class="btn cancel-btn" @click="cancelDialog">Cancel</button>
        <button class="btn save-btn" @click="savePrice">Save</button>
      </div>
    </el-dialog>

    <!-- Delete Confirm Dialog -->
    <el-dialog
      v-if="showDeleteDialog"
      title="Warning"
      :visible.sync="showDeleteDialog"
      width="30%"
      :close-on-click-modal="false"
    >
      <span>Are you sure you want to delete this stateroom price?</span>
      <div slot="footer" class="dialog-footer">
        <button class="btn cancel-btn" @click="showDeleteDialog = false">Cancel</button>
        <button class="btn delete-btn" @click="confirmDelete">Delete</button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import request from '../../utils/request'

const rooms = ref([])
const isLoading = ref(false)

const showDialog = ref(false)
const showDeleteDialog = ref(false)

const editingPriceId = ref(null)  // 用于区分是编辑还是新增
const deletingPriceId = ref(null) // 准备删除的价格ID

const formData = reactive({
  price_id: '',
  stateroom_id: '',
  trip_id: '',
  price_per_night: 0,
  is_vacant: false
})

onMounted(() => {
  fetchRooms()
})

async function fetchRooms() {
  isLoading.value = true
  try {
    const response = await request.get('/api/Admin/RoomPriceManage')
    isLoading.value = false
    rooms.value = response.stateroom_prices || []
  } catch (err) {
    console.error(err)
    alert('Error fetching stateroom prices')
    isLoading.value = false
  }
}

// 打开新增对话框
function openAddDialog() {
  editingPriceId.value = null
  resetForm()
  showDialog.value = true
}

// 打开编辑对话框
function openEditDialog(room) {
  editingPriceId.value = room.price_id
  formData.price_id = room.price_id
  formData.stateroom_id = room.stateroom_id
  formData.trip_id = room.trip_id
  formData.price_per_night = room.price_per_night
  formData.is_vacant = room.is_vacant
  showDialog.value = true
}

// 打开删除确认对话框
function openDeleteDialog(price_id) {
  deletingPriceId.value = price_id
  showDeleteDialog.value = true
}

// 确认删除操作
async function confirmDelete() {
  const price_id = deletingPriceId.value
  showDeleteDialog.value = false

  try {
    const response = await request.delete('/api/Admin/RoomPriceManage', { data: { price_id } })
    if (response.message && response.message.includes('deleted successfully')) {
      alert(`Stateroom price with ID ${price_id} deleted successfully.`)
      fetchRooms()
    } else {
      alert(response.message || 'Failed to delete stateroom price')
    }
  } catch (err) {
    console.error(err)
    alert('Error deleting stateroom price')
  }
}

// 保存价格（新增或编辑）
async function savePrice() {
  try {
    if (editingPriceId.value) {
      // 编辑操作，用PUT请求
      const response = await request.put('/api/Admin/RoomPriceManage', {
        price_id: formData.price_id,
        price_per_night: formData.price_per_night,
        is_vacant: formData.is_vacant
      })

      if (response.message && response.message.includes('updated successfully')) {
        alert(`Stateroom price with ID ${formData.price_id} updated successfully.`)
        showDialog.value = false
        fetchRooms()
      } else {
        alert(response.message || 'Failed to update stateroom price')
      }
    } else {
      // 新增操作，用POST请求
      if (!formData.stateroom_id || !formData.trip_id || formData.price_per_night == null) {
        alert('Please fill in all required fields.')
        return
      }

      const response = await request.post('/api/Admin/RoomPriceManage', {
        stateroom_id: formData.stateroom_id,
        price_per_night: formData.price_per_night,
        trip_id: formData.trip_id,
        is_vacant: formData.is_vacant
      })
      
      if (response.message && response.message.includes('created successfully')) {
        alert(`New stateroom price created successfully with ID ${response.price_id}.`)
        showDialog.value = false
        fetchRooms()
      } else {
        alert(response.message || 'Failed to create stateroom price')
      }
    }
  } catch (err) {
    console.error(err)
    alert('Error saving stateroom price')
  }
}

function cancelDialog() {
  showDialog.value = false
}

function resetForm() {
  formData.price_id = ''
  formData.stateroom_id = ''
  formData.trip_id = ''
  formData.price_per_night = 0
  formData.is_vacant = false
}
</script>

<style scoped>
.room-manage-container {
  background: #f5f8fa;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

.card {
  background: #fff;
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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

.top-actions {
  text-align: right;
  margin-bottom: 20px;
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
  font-size: 14px;
}

.room-table th, .room-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.room-table th {
  background: #f0f9ff;
  font-weight: bold;
  color: #007acc;
}

.room-table tbody tr:nth-child(even) {
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
  margin-left: 5px;
}

.btn:hover {
  background: #005f99;
}

.add-btn {
  background: #28a745;
}

.add-btn:hover {
  background: #218838;
}

.edit-btn {
  background: #ffc107;
  color: #333;
}

.edit-btn:hover {
  background: #e6a700;
}

.delete-btn {
  background: #ff4d4f;
}

.delete-btn:hover {
  background: #cc0000;
  color: #fff;
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

.field input[type="text"],
.field input[type="number"] {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.check-field {
  flex-direction: row;
  align-items: center;
}

.check-field label {
  margin-right: 10px;
  margin-bottom: 0;
}

.dialog-title {
  font-weight: bold;
  font-size: 18px;
  margin: 0;
}

.dialog-content {
  padding: 10px 0;
}

.dialog-footer {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.cancel-btn {
  background: #ccc;
}

.cancel-btn:hover {
  background: #aaa;
}

.save-btn {
  background: #007acc;
}

.save-btn:hover {
  background: #005f99;
}
</style>

<template>
  <div class="entertainment-container">
    <h2 class="header">Entertainment</h2>

    <div v-if="isLoading" class="loading">Loading entertainment information...</div>
    <div v-else-if="entertainments.length === 0">
      <el-empty description="No entertainment information available"></el-empty>
    </div>
    <div v-else class="entertainment-table">
      <table>
        <thead>
          <tr>
            <th>Entertainment Name</th>
            <th>Number of Units</th>
            <th>Floor</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ent in entertainments" :key="ent.entertain_id">
            <td>{{ ent.entertain_name }}</td>
            <td>{{ ent.num_units }}</td>
            <td>{{ ent.at_floor }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import request from '../../utils/request'

export default {
  name: 'Entertainment',
  setup() {
    const entertainments = ref([]) // 存储娱乐信息
    const isLoading = ref(false) // 加载状态

    onMounted(() => {
      fetchEntertainment() // 页面加载时获取数据
    })

    async function fetchEntertainment() {
      isLoading.value = true
      try {
        const response = await request.get('/api/Passenger/Entertainment')
        isLoading.value = false

        // 打印调试信息
        console.log('Response received:', response);

        // 确保返回数据格式正确并解析
          entertainments.value = response.map(ent => ({
            entertain_id: ent.entertain_id,
            entertain_name: ent.entertain_name,
            num_units: ent.num_units,
            at_floor: ent.at_floor,
          }))
        
      } catch (err) {
        isLoading.value = false
        console.error('Error fetching entertainment information:', err)
        alert('Error fetching entertainment information')
      }
    }

    return {
      entertainments,
      isLoading
    }
  }
}
</script>

<style scoped>
.entertainment-container {
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
  text-align: center;
  color: #666;
  font-size: 14px;
  margin: 20px 0;
}

.entertainment-table {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

thead {
  background: #007acc;
  color: #fff;
}

thead th {
  padding: 10px;
}

tbody tr {
  border-bottom: 1px solid #ddd;
}

tbody td {
  padding: 10px;
}

tbody tr:nth-child(even) {
  background: #f9f9f9;
}
</style>

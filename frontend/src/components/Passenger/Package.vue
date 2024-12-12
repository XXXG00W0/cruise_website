<template> 
  <div class="package-container">
    <h2 class="header">Available Packages</h2>

    <div v-if="isLoading" class="loading">Loading packages...</div>
    <div v-else-if="packages.length === 0">
      <el-empty description="No package information available"></el-empty>
    </div>
    <div v-else class="package-table-container">
      <table class="package-table">
        <thead>
          <tr>
            <th>Package Name</th>
            <th>Charge Type</th>
            <th>Price</th>
            <th>Buy</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pkg in packages" :key="pkg.package_id">
            <td>{{ pkg.pkg_name }}</td>
            <td>{{ pkg.pkg_charge_type }}</td>
            <td>${{ pkg.pkg_price }}</td>
            <td>
              <button class="btn order-btn" @click="goToPackageOrder(pkg.package_id)">Purchase</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
import { ref, onMounted } from 'vue'
import request from '../../utils/request'
import { useRouter } from 'vue-router'

export default {
  name: 'Package',
  setup() {
    const packages = ref([]) // 存储套餐信息
    const isLoading = ref(false) // 加载状态
    const router = useRouter()

    onMounted(() => {
      fetchPackages() // 页面加载时获取数据
    })

    async function fetchPackages() {
      isLoading.value = true
      try {
        const response = await request.get('/api/Passenger/Package')
        isLoading.value = false

        // 打印调试信息，逐个输出每个字段

          // 遍历 response
          packages.value = response.map(pkg =>({
            package_id: pkg.package_id,
            pkg_name: pkg.pkg_name,
            pkg_charge_type: pkg.pkg_charge_type,
            pkg_price: pkg.pkg_price,
          }));
          

      } catch (err) {
        isLoading.value = false
        console.error('Error fetching package information:', err)
        alert('Error fetching package information');
      }
    }
  
    function goToPackageOrder(package_id) {
        // 跳转到 PackageOrder.vue，并传入 packageId 作为 query 参数
        router.push({ path: '/Main/PackageOrder', query: { package_id } })
      }
  
      return {
        packages,
        isLoading,
        goToPackageOrder
      }
    }
  }
  </script>
  
  <style scoped>
  .package-container {
    max-width: 900px;
    margin: 50px auto;
    font-family: 'Roboto', sans-serif;
    text-align: center;
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
  
  .package-table-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  .package-table {
    width: 100%;
    max-width: 800px;
    border-collapse: collapse;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .package-table th,
  .package-table td {
    text-align: center;
    padding: 15px;
    border-bottom: 1px solid #ddd;
    font-size: 14px;
  }
  
  .package-table th {
    background-color: #007acc;
    color: #fff;
    font-size: 16px;
    font-weight: bold;
  }
  
  .package-table td {
    color: #333;
  }
  
  .package-table tbody tr:nth-child(odd) {
    background-color: #f9f9f9;
  }
  
  .package-table tbody tr:hover {
    background-color: #f1f8ff;
  }
  
  .order-btn {
    background: #28a745;
    color: #fff;
    border: none;
    border-radius: 20px;
    padding: 8px 15px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .order-btn:hover {
    background: #218838;
  }
  </style>
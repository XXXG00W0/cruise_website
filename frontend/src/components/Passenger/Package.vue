<template>
    <div class="package-container">
      <h2 class="header">Available Packages</h2>
  
      <div v-if="isLoading" class="loading">Loading packages...</div>
      <div v-else-if="packages.length === 0">
        <el-empty description="No package information available"></el-empty>
      </div>
      <div v-else class="package-list">
        <ul>
          <li v-for="pkg in packages" :key="pkg.package_id" class="package-item">
            <h3>{{ pkg.pkg_name }}</h3>
            <p><strong>Charge Type:</strong> {{ pkg.pkg_charge_type }}</p>
            <p><strong>Price:</strong> ${{ pkg.pkg_price }}</p>
            <button class="btn order-btn" @click="goToPackageOrder(pkg.package_id)">Purchase</button>
          </li>
        </ul>
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
      const packages = ref([])
      const isLoading = ref(false)
      const router = useRouter()
  
      onMounted(() => {
        fetchPackages()
      })
  
      async function fetchPackages() {
        isLoading.value = true
        try {
          const response = await request.get('/api/packages')
          isLoading.value = false
          if (response.code === 200) {
            packages.value = response.data.packages
          } else {
            alert(response.message || 'Failed to fetch package information')
          }
        } catch (err) {
          console.error(err)
          alert('Error fetching package information')
          isLoading.value = false
        }
      }
  
      function goToPackageOrder(packageId) {
        // 跳转到 PackageOrder.vue，并传入 packageId 作为 query 参数
        router.push({ path: '/Main/PackageOrder', query: { packageId } })
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
  
  .package-list {
    background:#fff;
    padding:20px;
    border-radius:10px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
  }
  
  .package-list ul {
    list-style:none;
    padding:0;
  }
  
  .package-item {
    background:#f9f9f9;
    padding:15px;
    border-radius:5px;
    margin-bottom:10px;
  }
  
  .package-item h3 {
    color:#007acc;
    margin-bottom:10px;
  }
  
  .order-btn {
    background:#28a745;
    color:#fff;
    border:none;
    border-radius:20px;
    padding:8px 15px;
    cursor:pointer;
    transition: background 0.3s;
  }
  
  .order-btn:hover {
    background:#218838;
  }
  </style>
  
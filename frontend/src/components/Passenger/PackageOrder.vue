<template>
    <div class="package-order-container">
      <h2 class="header">Purchase Package</h2>
      <div v-if="isLoading" class="loading">Loading package info...</div>
      <div v-else>
        <div v-if="!pkgInfo">
          <p>Failed to load package information.</p>
        </div>
        <div v-else>
          <div class="info-box">
            <p><strong>Package ID:</strong> {{ packageId }}</p>
            <p><strong>Name:</strong> {{ pkgInfo.pkg_name }}</p>
            <p><strong>Charge Type:</strong> {{ pkgInfo.pkg_charge_type }}</p>
            <p><strong>Price:</strong> ${{ pkgInfo.pkg_price }}</p>
          </div>
  
          <div class="form-section">
            <h3>Payment Information</h3>
            <div class="field">
              <label>Payment Method:</label>
              <select v-model="orderForm.payment_method">
                <option value="">Select a method</option>
                <option value="Credit Card">Credit Card</option>
                <option value="PayPal">PayPal</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="field">
              <label>Payment Amount (USD):</label>
              <input type="number" v-model.number="orderForm.pay_amount" placeholder="Enter amount" />
            </div>
          </div>
  
          <div class="buttons">
            <button class="btn confirm-btn" @click="confirmOrder">Confirm Purchase</button>
          </div>
        </div>
      </div>
  
      <div v-if="invoice && packageSale" class="result-section">
        <h3>Purchase Successful</h3>
        <p>You have successfully purchased this package!</p>
        <h4>Invoice Details:</h4>
        <p><strong>Invoice ID:</strong> {{ invoice.invoice_id }}</p>
        <p><strong>Billing Date/Time:</strong> {{ formatDateTime(invoice.billing_date_time) }}</p>
        <p><strong>Payment Due:</strong> ${{ invoice.payment_due }}</p>
  
        <h4>Package Sale Details:</h4>
        <p><strong>Package Sale ID:</strong> {{ packageSale.pkg_sale_id }}</p>
        <p><strong>Package ID:</strong> {{ packageSale.package_id }}</p>
        <p><strong>Group ID:</strong> {{ packageSale.group_id }}</p>
        <p><strong>Invoice ID:</strong> {{ packageSale.invoice_id }}</p>
  
        <div class="return-section">
          <p>You will be redirected to Main page soon...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import request from '../../utils/request'
  
  export default {
    name: 'PackageOrder',
    setup() {
      const route = useRoute()
      const router = useRouter()
  
      const packageId = route.query.packageId || ''
      const isLoading = ref(true)
      const pkgInfo = ref(null)
      const invoice = ref(null)
      const packageSale = ref(null)
  
      const orderForm = reactive({
        pay_amount: '',
        payment_method: ''
      })
  
      onMounted(() => {
        fetchPackageInfo()
      })
  
      async function fetchPackageInfo() {
        try {
          const response = await request.get(`/api/Passenger/PurchasePackage`)
          isLoading.value = false
          if (response.code === 200) {
            pkgInfo.value = response.data.package
          } else {
            alert(response.message || 'Failed to load package information')
          }
        } catch (err) {
          console.error(err)
          alert('Error loading package information')
          isLoading.value = false
        }
      }
  
      async function confirmOrder() {
        if (!orderForm.payment_method || !orderForm.pay_amount) {
          alert('Please fill in all required fields.')
          return
        }
  
        try {
          const response = await request.post('/api/purchase-package', {
            packageId,
            pay_amount: orderForm.pay_amount,
            payment_method: orderForm.payment_method
            // group_id can be handled by backend based on current user
          })
          if (response.code === 200) {
            alert('Purchase successful!')
            invoice.value = response.data.invoice
            packageSale.value = response.data.packageSale
  
            setTimeout(() => {
              router.push('/Main')
            }, 3000)
          } else {
            alert(response.message || 'Purchase failed')
          }
        } catch (err) {
          console.error(err)
          alert('Error purchasing package')
        }
      }
  
      function formatDateTime(dtStr) {
        if (!dtStr) return ''
        const date = new Date(dtStr)
        return date.toLocaleString()
      }
  
      return {
        packageId,
        isLoading,
        pkgInfo,
        invoice,
        packageSale,
        orderForm,
        confirmOrder,
        formatDateTime
      }
    }
  }
  </script>
  
  <style scoped>
  .package-order-container {
    width: 600px;
    margin: 50px auto;
    font-family: 'Roboto', sans-serif;
    background: #fff;
    padding: 30px;
    border-radius: 10px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
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
  
  .info-box {
    background:#f0f9ff;
    padding:10px;
    border-radius:5px;
    margin-bottom:20px;
  }
  
  .form-section {
    margin-top:20px;
  }
  
  .form-section h3 {
    color:#007acc;
    margin-bottom:10px;
    font-weight:bold;
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
  
  .field input, .field select {
    padding:8px;
    border:1px solid #ddd;
    border-radius:5px;
    font-size:14px;
  }
  
  .buttons {
    text-align:right;
    margin-top:20px;
  }
  
  .btn {
    padding:10px 20px;
    font-size:14px;
    background:#007acc;
    color:#fff;
    border:none;
    border-radius:20px;
    cursor:pointer;
    transition: background 0.3s;
    margin-left:10px;
  }
  
  .btn:hover {
    background:#005f99;
  }
  
  .result-section {
    margin-top:30px;
    background:#f7faff;
    padding:20px;
    border-radius:5px;
    text-align:center;
  }
  
  .result-section h3 {
    color:#28a745;
    margin-bottom:10px;
    font-weight:bold;
  }
  
  .result-section h4 {
    margin-top:20px;
    font-size:16px;
    font-weight:bold;
    text-align:left;
  }
  
  .result-section p {
    margin:5px 0;
    text-align:left;
  }
  
  .return-section {
    margin-top:20px;
    text-align:center;
    font-size:14px;
    color:#666;
  }
  </style>
  
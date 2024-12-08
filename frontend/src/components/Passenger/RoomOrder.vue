<template>
    <div class="room-order-container">
      <h2 class="header">Room Payment</h2>
      <div v-if="isLoading" class="loading">Loading price info...</div>
      <div v-else>
        <div v-if="!priceInfo">
          <p>Failed to load price information.</p>
        </div>
        <div v-else>
          <div class="info-box">
            <p><strong>Stateroom ID:</strong> {{ stateroomId }}</p>
            <p><strong>Trip ID:</strong> {{ tripId }}</p>
            <p><strong>Price per Night:</strong> ${{ priceInfo.pricePerNight }}</p>
            <p><strong>Vacancy:</strong> {{ priceInfo.isVacant ? 'Vacant' : 'Fully booked' }}</p>
            <p><strong>Beds per Stateroom:</strong> {{ priceInfo.num_bed }}</p>
          </div>
  
          <div class="form-section">
            <h3>Booking Information</h3>
            <div class="field">
              <label>Start Date:</label>
              <input type="date" v-model="orderForm.startDate" @change="calculateTotal" />
            </div>
            <div class="field">
              <label>End Date:</label>
              <input type="date" v-model="orderForm.endDate" @change="calculateTotal" />
            </div>
            <div class="field">
              <label>Number of group members older than 5:</label>
              <input type="number" min="0" v-model.number="orderForm.olderMembers" @input="calculateTotal" />
            </div>
            <div class="field">
              <label>Number of group members under 5:</label>
              <input type="number" min="0" v-model.number="orderForm.youngerMembers" />
            </div>
  
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
  
            <p v-if="orderForm.pay_amount > 0">
              <strong>Total Amount:</strong> ${{ orderForm.pay_amount }}
            </p>
          </div>
  
          <div class="buttons">
            <button class="btn confirm-btn" @click="confirmOrder">Confirm Payment</button>
          </div>
        </div>
      </div>
  
      <div v-if="invoice && payment && group" class="result-section">
        <h3>Payment Successful</h3>
        <p>Your room has been booked and paid successfully!</p>
        <h4>Invoice Details:</h4>
        <p><strong>Invoice ID:</strong> {{ invoice.invoice_id }}</p>
        <p><strong>Billing Date/Time:</strong> {{ formatDateTime(invoice.billing_date_time) }}</p>
        <p><strong>Payment Due:</strong> ${{ invoice.payment_due }}</p>
  
        <h4>Payment Details:</h4>
        <p><strong>Payment ID:</strong> {{ payment.payment_id }}</p>
        <p><strong>Payment Date:</strong> {{ formatDateTime(payment.payment_date) }}</p>
        <p><strong>Amount:</strong> ${{ payment.pay_amount }}</p>
        <p><strong>Method:</strong> {{ payment.payment_method }}</p>
  
        <h4>Group Details:</h4>
        <p><strong>Group ID:</strong> {{ group.group_id }}</p>
        
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
    name: 'RoomOrder',
    setup() {
      const route = useRoute()
      const router = useRouter()
  
      const stateroomId = route.query.stateroomId || ''
      const tripId = route.query.tripId || ''
  
      const isLoading = ref(true)
      const priceInfo = ref(null)
      const invoice = ref(null)
      const payment = ref(null)
      const group = ref(null)
  
      const orderForm = reactive({
        startDate: '',
        endDate: '',
        olderMembers: 0,
        youngerMembers: 0,
        pay_amount: 0,
        payment_method: ''
      })
  
      onMounted(() => {
        fetchPriceInfo()
      })
  
      async function fetchPriceInfo() {
        try {
          const response = await request.get(`/api/stateroom-price/${stateroomId}`, {
            params: { tripId: tripId }
          })
          isLoading.value = false
          if (response.code === 200) {
            // Assume response.data.price includes fields: pricePerNight, isVacant, num_bed
            priceInfo.value = response.data.price
          } else {
            alert(response.message || 'Failed to fetch stateroom price info')
          }
        } catch (err) {
          console.error(err)
          alert('Error fetching stateroom price info')
          isLoading.value = false
        }
      }
  
      function calculateTotal() {
        if (!orderForm.startDate || !orderForm.endDate || !priceInfo.value) {
          orderForm.pay_amount = 0
          return
        }
  
        const start = new Date(orderForm.startDate)
        const end = new Date(orderForm.endDate)
        const diff = end - start
        if (diff <= 0) {
          orderForm.pay_amount = 0
          return
        }
  
        const nights = Math.ceil(diff / (1000 * 60 * 60 * 24))
        const older = orderForm.olderMembers || 0
        const beds = priceInfo.value.num_bed
        // At least one stateroom
        let roomsNeeded = older > 0 ? Math.ceil(older / beds) : 1
        if (roomsNeeded < 1) roomsNeeded = 1
  
        orderForm.pay_amount = roomsNeeded * priceInfo.value.pricePerNight * nights
      }
  
      async function confirmOrder() {
        if (!orderForm.startDate || !orderForm.endDate || !orderForm.payment_method || orderForm.pay_amount <= 0) {
          alert('Please fill in all required fields and ensure amount is calculated.')
          return
        }
  
        try {
          const response = await request.post('/api/book-stateroom-order', {
            stateroomId,
            tripId,
            startDate: orderForm.startDate,
            endDate: orderForm.endDate,
            olderMembers: orderForm.olderMembers,
            youngerMembers: orderForm.youngerMembers,
            pay_amount: orderForm.pay_amount,
            payment_method: orderForm.payment_method
          })
          if (response.code === 200) {
            alert('Payment successful!')
            invoice.value = response.data.invoice
            payment.value = response.data.payment
            group.value = response.data.group // Assume backend returns group info after order
  
            // Redirect back to Main after a short delay
            setTimeout(() => {
              router.push('/Main')
            }, 3000)
          } else {
            alert(response.message || 'Booking failed')
          }
        } catch (err) {
          console.error(err)
          alert('Error booking stateroom')
        }
      }
  
      function formatDateTime(dtStr) {
        if (!dtStr) return ''
        const date = new Date(dtStr)
        return date.toLocaleString()
      }
  
      return {
        stateroomId,
        tripId,
        isLoading,
        priceInfo,
        invoice,
        payment,
        group,
        orderForm,
        confirmOrder,
        calculateTotal,
        formatDateTime
      }
    }
  }
  </script>
  
  <style scoped>
  .room-order-container {
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
  
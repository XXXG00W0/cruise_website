<template>
    <div class="container">
      <div class="item">
        <div class="name">Stateroom Number: {{ stateroom.room_number }}</div>
        <div class="info">
          <span class="detail-item">Location: {{ stateroom.location }}</span>
          <span class="detail-item">Beds: {{ stateroom.num_bed }}</span>
          <span class="detail-item">Bathrooms: {{ stateroom.num_bathroom }}</span>
          <span class="detail-item">Balconies: {{ stateroom.num_balcony }}</span>
          <span class="detail-item">Size: {{ stateroom.size_sqft }} sqft</span>
        </div>
        <img :src="coverImage" alt="Stateroom Image" />
        <div class="extra-info">
          <span class="address">Stateroom detail information above.</span>
        </div>
      </div>
      <div>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="Price & Booking" name="priceBooking">
            <div v-if="isLoadingPrice" class="loading">Loading price information...</div>
            <div v-else-if="prices.length === 0">
              <el-empty description="No price info available"></el-empty>
            </div>
            <div v-else>
              <div class="room-item" v-for="(priceItem, index) in prices" :key="index">
                <div class="name">Trip ID: {{ priceItem.trip_id }}</div>
                <div class="bottom">
                  <div class="price-section">
                    <div style="margin-bottom: 6px;">
                      <span class="price">
                        Price per night: ${{ priceItem.price_per_night }}
                      </span>
                      <span class="vacancy" :style="{color: priceItem.is_vacant == 1 ? 'green' : 'red'}">
                        {{ priceItem.is_vacant == 1 ? 'Vacant' : 'Fully booked' }}
                      </span>
                    </div>
                    <div class="detail">
                      Additional room details above.
                    </div>
                    <div style="margin-top: 6px;">
                      <!-- If vacant, show a button to go to RoomOrder.vue -->
                      <span class="order-room" v-if="priceItem.is_vacant == 1" @click="goToRoomOrder(priceItem)">
                        Go to Order Page
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios' // or import request from '../../utils/request' if needed
  
  export default {
    name: "RoomDetail",
    setup() {
      const route = useRoute()
      const router = useRouter()
  
      const stateroom = reactive({})
      const prices = ref([])
      const activeName = ref('first')
      const coverImage = 'https://example.com/stateroom_default.jpg' // Replace if needed
      const isLoadingPrice = ref(false)
  
      onMounted(() => {
        loadInfo()
      })
  
      function handleClick(tab, event) {
        if (tab.name === 'priceBooking') {
          fetchPriceInfo()
        }
      }
  
      function fetchPriceInfo() {
        if (!stateroom.stateroom_id) return
        isLoadingPrice.value = true
        axios.post('/stateroomPrice/query', { stateroom_id: stateroom.stateroom_id })
          .then(res => {
            isLoadingPrice.value = false
            if (res.data.code === 200) {
              prices.value = res.data.data
            } else {
              alert('Failed to fetch price info')
            }
          })
          .catch(error => {
            isLoadingPrice.value = false
            console.log(error)
            alert('Error fetching price info')
          })
      }
  
      function loadInfo() {
        const jsonInfo = sessionStorage.getItem('stateroomInfo')
        const info = JSON.parse(jsonInfo) || {}
        Object.assign(stateroom, info)
      }
  
      function goToRoomOrder(priceItem) {
        // Navigate to RoomOrder.vue with stateroom_id and trip_id as query params
        router.push({ 
          path: '/Main/RoomOrder', 
          query: { 
            stateroomId: stateroom.stateroom_id, 
            tripId: priceItem.trip_id 
          } 
        })
      }
  
      return {
        stateroom,
        prices,
        activeName,
        coverImage,
        isLoadingPrice,
        handleClick,
        goToRoomOrder
      }
    }
  }
  </script>
  
  <style scoped>
  .container {
    width: 800px;
    margin: 0 auto;
  }
  
  .item {
    background-color: rgb(248, 246, 246);
    padding: 16px;
    border-radius: 5px;
    margin-bottom: 20px;
  }
  
  .name {
    font-size: 36px;
    margin-block: 10px;
    font-weight: 800;
  }
  
  .info {
    display: flex;
    justify-content: left;
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .detail-item {
    font-size: 14px;
    color: #333;
  }
  
  .extra-info {
    margin-block: 10px;
  }
  
  .address {
    font-size: 14px;
    color: rgb(28, 89, 186);
  }
  
  .room-item {
    background-color: rgb(246, 246, 246);
    padding: 16px;
    box-sizing: border-box;
    margin-bottom: 4px;
    border-radius: 5px;
  }
  
  .room-item .name {
    font-size: 24px;
    margin-block: 10px;
    font-weight: 800;
  }
  
  .bottom {
    display: flex;
    justify-content: flex-start;
    gap: 8px;
  }
  
  .price-section .price {
    font-size: 24px;
    font-weight: 800;
    color: rgb(227, 152, 99);
  }
  
  .order-room {
    display: inline-block;
    padding: 4px 10px;
    background-color: rgb(75, 105, 207);
    border-radius: 2px;
    font-size: 12px;
    color: aliceblue;
    cursor: pointer;
  }
  
  .order-room:hover {
    background-color: rgb(29, 64, 179);
  }
  
  .detail {
    font-size: 12px;
    color: rgb(139, 138, 138);
  }
  
  .loading {
    text-align: center;
    color: #666;
    font-size: 14px;
    margin: 20px 0;
  }
  </style>
  
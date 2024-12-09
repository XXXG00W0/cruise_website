<template>
  <div class="container">
    <div class="item" v-if="stateroom">
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
      <button class="order-button" @click="goToRoomOrder">Go to Order Page</button>
    </div>
    <div v-else>
      <div class="loading">Loading stateroom information...</div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

export default {
  name: "RoomDetail",
  setup() {
    const route = useRoute();
    const router = useRouter();

    const stateroom = reactive({});
    const coverImage = "https://example.com/stateroom_default.jpg"; // Replace if needed
    const isLoading = ref(true);

    onMounted(() => {
      const trip_id = route.query.trip_id; // 从路由参数中获取 trip_id
      if (trip_id) {
        fetchStateroomDetails(trip_id);
      }
    });

    function fetchStateroomDetails(trip_id) {
      axios
        .get(`/Passenger/RoomDetail`, { params: { trip_id } })
        .then((res) => {
          if (res.status === 200) {
            Object.assign(stateroom, res.data); // 将获取的数据存入 stateroom
            isLoading.value = false;
          } else {
            alert("Failed to fetch stateroom details.");
            isLoading.value = false;
          }
        })
        .catch((error) => {
          console.error(error);
          alert("Error fetching stateroom details.");
          isLoading.value = false;
        });
    }

    function goToRoomOrder() {
      router.push({
        path: "/Main/RoomOrder",
        query: {
          stateroomId: stateroom.stateroom_id,
          tripId: route.query.trip_id,
        },
      });
    }

    return {
      stateroom,
      coverImage,
      isLoading,
      goToRoomOrder,
    };
  },
};
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
  flex-wrap: wrap;
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

.order-button {
  padding: 10px 20px;
  background-color: rgb(75, 105, 207);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
}

.order-button:hover {
  background-color: rgb(29, 64, 179);
}

.loading {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin: 20px 0;
}
</style>

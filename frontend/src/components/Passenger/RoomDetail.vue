<template>
  <div class="restaurant-container">
    <h2 class="header">Staterooms Detail</h2>

    <div v-if="isLoading" class="loading">Loading staterooms...</div>
    <div v-else-if="stateroom.length === 0">
      <el-empty description="No staterooms information available"></el-empty>
    </div>
    <div v-else class="staterooms-table">
      <table>
        <thead>
          <tr>
            <th>Room Number</th>
            <th>Location</th>
            <th>Bed Number</th>
            <th>Bathroom Number</th>
            <th>Balcony Number</th>
            <th>Size (sqft)</th>
            <th>Price per Night</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="room in stateroom" :key="room.stateroom_id">
            <td>{{ room.room_number }}</td>
            <td>{{ room.location }}</td>
            <td>{{ room.num_bed }}</td>
            <td>{{ room.num_bathroom }}</td>
            <td>{{ room.num_balcony }}</td>
            <td>{{ room.size_sqft }}</td>
            <td>{{ room.price_per_night }}</td>
            <td>
              <button class="order-button" @click="goToRoomOrder(room)">Order</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import request from "../../utils/request";

export default {
  name: "RoomDetail",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const trip_id = route.query.trip_id || "";
    const stateroom = ref([]);
    const isLoading = ref(false);

    onMounted(() => {
      fetchStateroomDetails(trip_id);
    });

    async function fetchStateroomDetails(trip_id) {
      isLoading.value = true;
      try {
        const response = await request.get("/api/Passenger/RoomDetail", {
          params: { trip_id },
        });
        stateroom.value = response.map((room) => ({
          stateroom_id: room.stateroom_id,
          room_number: room.room_number,
          location: room.location,
          num_bed: room.num_bed,
          num_bathroom: room.num_bathroom,
          num_balcony: room.num_balcony,
          size_sqft: room.size_sqft,
          price_per_night: room.price_per_night,
        }));
      } catch (err) {
        console.error("Error fetching stateroom details:", err);
        alert("Error fetching stateroom details.");
      } finally {
        isLoading.value = false;s
      }
    }

    function goToRoomOrder(room) {
      router.push({
        path: "/Main/RoomOrder",
        query: {
          stateroomId: room.stateroom_id,
          tripId: route.query.trip_id,
        },
      });
    }

    return {
      stateroom,
      isLoading,
      goToRoomOrder,
    };
  },
};
</script>

<style scoped>
.restaurant-container {
  max-width: 900px;
  margin: 0 auto;
}

.header {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.staterooms-table table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.staterooms-table th,
.staterooms-table td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}

.staterooms-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.staterooms-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.order-button {
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.order-button:hover {
  background-color: #45a049;
}

.loading {
  text-align: center;
  font-size: 16px;
  color: #666;
  margin: 20px 0;
}
</style>

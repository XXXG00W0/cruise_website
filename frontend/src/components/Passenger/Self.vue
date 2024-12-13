<template>
  <div class="self-container">
    <h2 class="header">My Profile</h2>
    <div v-if="isLoading" class="loading">Loading your information...</div>
    <div v-else>
      <div v-if="!passenger">
        <p>Failed to load your profile information.</p>
      </div>
      <div v-else class="info-box">
        <h3>Personal Information</h3>
        <!-- Displaying read-only fields -->
        <p><strong>Name (read-only):</strong> {{ passenger.first_name }} {{ passenger.last_name }}</p>
        <p><strong>User ID (read-only):</strong> {{ passenger.id }}</p>

        <h3>Editable Fields</h3>
        <div class="field">
          <label>Phone:</label>
          <input type="text" v-model="editForm.phone" />
        </div>

        <h3>Address Information</h3>
        <div class="field">
          <label>Street:</label>
          <input type="text" v-model="editForm.street" />
        </div>
        <div class="field">
          <label>City:</label>
          <input type="text" v-model="editForm.city" />
        </div>
        <div class="field">
          <label>State/Province:</label>
          <input type="text" v-model="editForm.state_province" />
        </div>
        <div class="field">
          <label>Postal Code:</label>
          <input type="text" v-model="editForm.postal_code" />
        </div>
        <div class="field">
          <label>Country:</label>
          <input type="text" v-model="editForm.country" />
        </div>

        <div class="buttons">
          <button class="btn save-btn" @click="updatePersonalInfo">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import request from '../../utils/request'

export default {
  name: 'Self',
  setup() {
    const passenger = ref(null)
    const isLoading = ref(false)

    const editForm = reactive({
      phone: '',
      street: '',
      city: '',
      state_province: '',
      postal_code: '',
      country: ''
    })

    onMounted(() => {
      fetchPassengerInfo()
    })

    async function fetchPassengerInfo() {
      isLoading.value = true
      try {
        const response = await request.get('/api/Passenger/Self')
        isLoading.value = false
        // Assuming response: { passenger: {...} }
        passenger.value = response.passenger
        if (passenger.value) {
          // Initialize form fields with existing data
          editForm.phone = passenger.value.phone || ''
          const addr = passenger.value.address || {}
          editForm.street = addr.street || ''
          editForm.city = addr.city || ''
          editForm.state_province = addr.state_province || ''
          editForm.postal_code = addr.postal_code || ''
          editForm.country = addr.country || ''
        } else {
          alert('Failed to fetch passenger info')
        }
      } catch (err) {
        console.error(err)
        alert('Error fetching passenger info')
        isLoading.value = false
      }
    }

    async function updatePersonalInfo() {
      try {
        // Send all fields top-level as the backend expects
        const payload = {
          first_name: passenger.value ? passenger.value.first_name : '',
          last_name: passenger.value ? passenger.value.last_name : '',
          phone: editForm.phone,
          street: editForm.street,
          city: editForm.city,
          state_province: editForm.state_province,
          postal_code: editForm.postal_code,
          country: editForm.country
        }

        const response = await request.put('/api/Passenger/Self', payload)

        // The server returns a JSON with { "message": "..."} on success
        if (response && response.message) {
          alert(response.message)
          // Update the local data to reflect changes
          if (passenger.value) {
            passenger.value.phone = editForm.phone
            if (passenger.value.address) {
              passenger.value.address.street = editForm.street
              passenger.value.address.city = editForm.city
              passenger.value.address.state_province = editForm.state_province
              passenger.value.address.postal_code = editForm.postal_code
              passenger.value.address.country = editForm.country
            }
          }
        } else {
          alert('Failed to update personal info')
        }
      } catch (err) {
        console.error(err)
        alert('Error updating personal info')
      }
    }

    return {
      passenger,
      isLoading,
      editForm,
      updatePersonalInfo
    }
  }
}
</script>

<style scoped>
.self-container {
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
  padding:20px;
  border-radius:5px;
}

.info-box h3 {
  color:#007acc;
  margin-bottom:10px;
  font-weight:bold;
  margin-top:20px;
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

.field input {
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
</style>

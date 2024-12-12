<template>
    <div class="itinerary-manage-container">
      <h1>Itinerary Management</h1>
  
      <div class="itinerary-form-section">
        <h2>{{ isEditing ? "Edit Itinerary" : "Add New Itinerary" }}</h2>
        <form @submit.prevent="handleSubmit" class="form-grid">
          <div class="form-group">
            <label for="trip_id">Trip ID:</label>
            <input type="text" v-model="form.trip_id" id="trip_id" required />
          </div>
  
          <div class="form-group">
            <label for="port_id">Port ID:</label>
            <input type="text" v-model="form.port_id" id="port_id" required />
          </div>
  
          <div class="form-group">
            <label for="arrival_date_time">Arrival Date/Time (YYYY-MM-DD HH:mm:ss):</label>
            <input type="text" v-model="form.arrival_date_time" id="arrival_date_time" required />
          </div>
  
          <div class="form-group">
            <label for="leaving_date_time">Leaving Date/Time (YYYY-MM-DD HH:mm:ss):</label>
            <input type="text" v-model="form.leaving_date_time" id="leaving_date_time" required />
          </div>
  
          <div class="button-group">
            <button type="submit" class="btn-primary">
              {{ isEditing ? "Update Itinerary" : "Add Itinerary" }}
            </button>
            <button type="button" v-if="isEditing" @click="cancelEdit" class="btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
  
      <hr />
  
      <div class="itinerary-table-section">
        <h2>Existing Itineraries</h2>
        <table class="itinerary-table">
          <thead>
            <tr>
              <th>Itinerary ID</th>
              <th>Trip ID</th>
              <th>Port ID</th>
              <th>Arrival Time</th>
              <th>Leaving Time</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="itinerary in itineraries" :key="itinerary.itinerary_id">
              <td>{{ itinerary.itinerary_id }}</td>
              <td>{{ itinerary.trip_id }}</td>
              <td>{{ itinerary.port_id }}</td>
              <td>{{ itinerary.arrival_date_time }}</td>
              <td>{{ itinerary.leaving_date_time }}</td>
              <td class="actions-cell">
                <button @click="editItinerary(itinerary)" class="btn-secondary">Edit</button>
                <button @click="deleteItinerary(itinerary.itinerary_id)" class="btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
  
        <div v-if="error" class="message error-message">
          <p>{{ error }}</p>
        </div>
        <div v-if="successMessage" class="message success-message">
          <p>{{ successMessage }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'ItineraryManage',
    data() {
      return {
        itineraries: [],
        form: {
          itinerary_id: null,
          trip_id: '',
          port_id: '',
          arrival_date_time: '',
          leaving_date_time: ''
        },
        isEditing: false,
        error: null,
        successMessage: null
      }
    },
    created() {
      this.fetchItineraries()
    },
    methods: {
      async fetchItineraries() {
        this.error = null
        this.successMessage = null
        try {
          const response = await axios.get('/api/Admin/ManageItinerary')
          console.log('response',response)
          if (response ) {
            this.itineraries = response.data.itineraries || []
            
          } else {
            this.itineraries = []
          }
        } catch (err) {
          console.error(err)
          this.error = 'Failed to fetch itineraries.'
        }
      },
      async handleSubmit() {
        this.error = null
        this.successMessage = null
        const payload = {
          trip_id: this.form.trip_id,
          port_id: this.form.port_id,
          arrival_date_time: this.form.arrival_date_time,
          leaving_date_time: this.form.leaving_date_time
        }
  
        try {
          if (this.isEditing && this.form.itinerary_id) {
            // Update itinerary
            payload.itinerary_id = this.form.itinerary_id
            await axios.put('/api/Admin/ManageItinerary', payload)
            this.successMessage = 'Itinerary updated successfully!'
          } else {
            // Add new itinerary
            await axios.post('/api/Admin/ManageItinerary', payload)
            this.successMessage = 'Itinerary added successfully!'
          }
          this.fetchItineraries()
          this.resetForm()
        } catch (err) {
          console.error(err)
          this.error = (err.response && (err.response.error || err.response.message)) 
                       || 'Operation failed. Please check your input to make sure no conflict between times.'
        }
      },
      async deleteItinerary(itinerary_id) {
        this.error = null
        this.successMessage = null
        try {
          await axios.delete('/api/Admin/ManageItinerary', { data: { itinerary_id } })
          this.successMessage = 'Itinerary deleted successfully!'
          this.fetchItineraries()
        } catch (err) {
          console.error(err)
          this.error = (err.response  && (err.response.error || err.response.message)) 
                       || 'Delete operation failed.'
        }
      },
      editItinerary(itinerary) {
        this.isEditing = true
        this.form.itinerary_id = itinerary.itinerary_id
        this.form.trip_id = itinerary.trip_id
        this.form.port_id = itinerary.port_id
        this.form.arrival_date_time = itinerary.arrival_date_time
        this.form.leaving_date_time = itinerary.leaving_date_time
      },
      cancelEdit() {
        this.isEditing = false
        this.resetForm()
      },
      resetForm() {
        this.form.itinerary_id = null
        this.form.trip_id = ''
        this.form.port_id = ''
        this.form.arrival_date_time = ''
        this.form.leaving_date_time = ''
        this.isEditing = false
      }
    }
  }
  </script>
  
  <style scoped>
  .itinerary-manage-container {
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .itinerary-form-section {
    margin-bottom: 30px;
  }
  
  .form-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 15px;
    max-width: 400px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .form-group label {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  input[type="text"] {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .button-group {
    display: flex;
    gap: 10px;
    align-items: center;
  }
  
  .btn-primary, .btn-secondary, .btn-danger {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: #1b9aaa;
    color: #fff;
  }
  
  .btn-secondary {
    background-color: #6c757d;
    color: #fff;
  }
  
  .btn-danger {
    background-color: #dc3545;
    color: #fff;
  }
  
  .itinerary-table-section {
    margin-top: 30px;
  }
  
  .itinerary-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .itinerary-table th, .itinerary-table td {
    border: 1px solid #ddd;
    text-align: left;
    padding: 10px;
  }
  
  .itinerary-table th {
    background-color: #f8f9fa;
    font-weight: bold;
  }
  
  .actions-cell {
    display: flex;
    gap: 10px;
  }
  
  .message {
    margin-top: 10px;
    font-weight: bold;
    padding: 10px;
    border-radius: 4px;
  }
  
  .error-message {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .success-message {
    background-color: #d4edda;
    color: #155724;
  }
  </style>
  
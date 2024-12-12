<template>
    <div class="board-container">
      <h2 class="title">Data Visualization</h2>
      <p class="subtitle">Here are your current stats:</p>
  
      <div class="cards-container">
        <div class="stat-card">
          <h3>Registered Users</h3>
          <p class="stat-value">{{ dashboardData.registered_users }}</p>
        </div>
        <div class="stat-card">
          <h3>Listed Staterooms</h3>
          <p class="stat-value">{{ dashboardData.listed_staterooms }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Bookings</h3>
          <p class="stat-value">{{ dashboardData.total_bookings }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Trips</h3>
          <p class="stat-value">{{ dashboardData.total_trips }}</p>
        </div>
        <div class="stat-card">
          <h3>Package Sales</h3>
          <p class="stat-value">{{ dashboardData.total_package }}</p>
        </div>
      </div>
  
      <div class="chart-container">
        <h3 class="chart-title">Cruise Stats Overview</h3>
        <BarChart :chart-data="chartData" :chart-options="chartOptions" />
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import request from '../../utils/request';
import { BarChart } from 'vue-chart-3';
import { Chart, BarElement, CategoryScale, LinearScale, LogarithmicScale, Title, Tooltip, Legend, BarController } from 'chart.js';

// Register necessary Chart.js components
Chart.register(BarController, BarElement, CategoryScale, LinearScale, LogarithmicScale, Title, Tooltip, Legend);

const dashboardData = ref({
  registered_users: 0,
  listed_staterooms: 0,
  total_bookings: 0,
  total_trips: 0,
  total_package: 0,
});

const chartData = ref({
  labels: [],
  datasets: [],
});

const chartOptions = ref({
  indexAxis: 'y',
  responsive: true,
  scales: {
    x: {
      title: {
        display: true,
        text: 'Metrics',
      },
    },
    y: {
      type: 'logarithmic', // Set y-axis to logarithmic
      title: {
        display: true,
        text: 'Count',
      },
      ticks: {
        callback: function (value) {
          return value.toLocaleString(); // Format tick values
        },
      },
    },
  },
  plugins: {
    title: {
      display: true,
      text: 'Overview of Key Metrics',
      font: {
        size: 18,
      },
    },
    legend: {
      display: false,
    },
  },
});

onMounted(async () => {
  await fetchDashboardData();
  updateChartData();
});

async function fetchDashboardData() {
  try {
    const response = await request.get('/api/Admin/Board');
    dashboardData.value = response.dashboard_data;
  } catch (err) {
    console.error(err);
    alert('Error fetching dashboard data');
  }
}

function updateChartData() {
  const { registered_users, listed_staterooms, total_bookings, total_trips, total_package } = dashboardData.value;
  chartData.value = {
    labels: ['Registered Users', 'Listed Staterooms', 'Total Bookings', 'Total Trips', 'Total Package'],
    datasets: [
      {
        label: 'Count',
        data: [registered_users, listed_staterooms, total_bookings, total_trips, total_package],
        backgroundColor: ['#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f'],
      },
    ],
  };
}
</script>

<style scoped>
.board-container {
  padding: 20px;
  background: #f5f8fa;
  min-height: 100vh;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

.title {
  font-size: 24px;
  color: #007acc;
  font-weight: bold;
  margin-bottom: 5px;
  text-align: center;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.cards-container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin-bottom: 40px;
}

.stat-card {
  background: linear-gradient(135deg, #9c6fcb, #5c6ac4);
  color: #fff;
  border-radius: 10px;
  padding: 20px;
  width: 200px;
  text-align: center;
  margin: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  font-size: 16px;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
}

.chart-container {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  max-width: 800px;
  margin: 0 auto;
}

.chart-title {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}
</style>
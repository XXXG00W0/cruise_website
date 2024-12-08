import { createRouter, createWebHashHistory } from 'vue-router'

import Login from '../components/Login.vue'
import Regist from '../components/Regist.vue'
import Main from '../components/Passenger/Main.vue'
import Board from '../components/Admin/Board.vue'
import RoomDetail from '../components/Passenger/RoomDetail.vue'
import Trip from '../components/Passenger/Trip.vue'
import MyTrip from '../components/Passenger/MyTrip.vue'
import Entertainment from '../components/Passenger/Entertainment.vue'
import Package from '../components/Passenger/Package.vue'
import PackageOrder from '../components/Passenger/PackageOrder.vue'
import RoomOrder from '../components/Passenger/RoomOrder.vue'
import Restraunt from '../components/Passenger/Restaurant.vue' 
import Self from '../components/Passenger/Self.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      component: Login
    },
    {
      path: '/Main',
      component: Main,
      children: [
        {
          path: 'RoomDetail',
          component: RoomDetail
        },
        {
          path: 'Trip',
          component: Trip
        },
        {
          path: 'MyTrip',
          component: MyTrip
        },
        {
          path: 'Entertainment',
          component: Entertainment
        },
        {
          path: 'Package',
          component: Package
        },
        {
          path: 'PackageOrder',
          component: PackageOrder
        },
        {
          path: 'RoomOrder',
          component: RoomOrder
        },
        {
          path: 'Restraunt',
          component: Restraunt
        },
        {
          path: 'Self',
          component: Self
        }
      ]
    },
    {
      path: '/login',
      component: Login 
    },
    {
      path: '/regist',
      component: Regist 
    },
    {
      path: '/admin',
      component: Board 
    }
  ]
})

export default router

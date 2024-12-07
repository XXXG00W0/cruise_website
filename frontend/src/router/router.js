import {createRouter, createWebHashHistory} from 'vue-router'

import Login from '../components/Login.vue'
import Regist from '../components/Regist.vue'
import Home from '../components/Home.vue'
import Admin from '../components/Admin.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            component: Login
        },
        {
            path: '/home',
            component: Home 
        },
        {
            path: '/login',
            component: Login 
        },        {
            path: '/regist',
            component: Regist 
        },        {
            path: '/admin',
            component: Admin 
        }
    ]
})
export default router;
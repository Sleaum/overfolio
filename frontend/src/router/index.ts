import { createRouter, createWebHistory } from 'vue-router'
import GoogleSheet from '@/views/GoogleSheet.vue'

const routes = [
  { path: '/', redirect: '/googlesheet' },
  { path: '/googlesheet', name: 'GoogleSheet', component: GoogleSheet }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router


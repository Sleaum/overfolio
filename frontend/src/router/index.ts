import { createRouter, createWebHistory } from 'vue-router'
import HeroSection from '../components/HeroSection.vue'
import NewPage from '../components/NewPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HeroSection },
  { path: '/newpage', name: 'NewPage', component: NewPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router


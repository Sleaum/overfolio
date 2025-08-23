import { createRouter, createWebHistory } from 'vue-router'
import HeroSection from '../components/HeroSection.vue'
import NewPage from '../components/NewPage.vue'
import SheetPage from '../components/SheetPage.vue'
import EchartPage from '../components/EchartPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HeroSection },
  { path: '/newpage', name: 'NewPage', component: NewPage },
  { path: '/sheet', name: 'SheetPage', component: SheetPage },
  { path: '/echart', name: 'EchartPage', component: EchartPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router


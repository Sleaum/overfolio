import { createRouter, createWebHistory } from 'vue-router'
import HeroSection from '../views/HeroSection.vue'
import NewPage from '../views/NewPage.vue'
import SheetPage from '../views/SheetPage.vue'
import EchartPage from '../views/EchartPage.vue'
import BoardPage from '../views/DashboardPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HeroSection },
  { path: '/newpage', name: 'NewPage', component: NewPage },
  { path: '/sheet', name: 'SheetPage', component: SheetPage },
  { path: '/echart', name: 'EchartPage', component: EchartPage },
  { path: '/board', name: 'BoardPage', component: BoardPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router


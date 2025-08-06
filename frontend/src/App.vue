<template>
  <div>
    <h1>Dashboard</h1>
    <TodayTable :data="todayData" />
    <EChartComponent :data="todayData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TodayTable from './components/TodayTable.vue'
import EChartComponent from './components/EChartComponent.vue'

const todayData = ref([])

const fetchData = async () => {
  try {
    const res = await fetch('/api/googlesheet/?doc_name=overfolio')
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
    const json = await res.json()
    todayData.value = json.today || []
  } catch (err) {
    console.error('Fetch error:', err)
  }
}

onMounted(() => {
  fetchData()
})
</script>


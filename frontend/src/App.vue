<template>
  <div>
    <h1>Dashboard</h1>
    <TodayTable />
    <EChartComponent :data="todayData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TodayTable from './components/TodayTable.vue';
import EChartComponent from './components/EChartComponent.vue'

const todayData = ref([])

const fetchData = async () => {
  const res = await fetch('http://localhost:8000/api/googlesheet/?doc_name=overfolio')
  const json = await res.json()
  // Si tes données sont dans json.today, sinon adapte
  todayData.value = json.today || []
}

onMounted(() => {
  fetchData()
})
</script>


<template>
  <div ref="chart" style="width: 600px; height: 400px;"></div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

const chart = ref(null)
let myChart = null

const initChart = () => {
  if (!chart.value) return
  myChart = echarts.init(chart.value)

  // Construis ici les options de ton graphique à partir de props.data
  const option = {
    xAxis: {
      type: 'category',
      data: props.data.map(item => item.Date)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: props.data.map(item => Number(item.Quantité) || 0),
        type: 'line',
        smooth: true
      }
    ]
  }

  myChart.setOption(option)
}

onMounted(() => {
  initChart()
})

watch(() => props.data, () => {
  if (myChart) {
    initChart()
  }
})
</script>


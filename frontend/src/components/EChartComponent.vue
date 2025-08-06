<template>
  <v-chart :option="chartOption" style="width: 600px; height: 400px;" />
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'

// Import des modules nécessaires (modulaire pour echarts 5)
import { LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent } from 'echarts/components'

// Enregistre les modules auprès de echarts
use([LineChart, CanvasRenderer, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

// Props attendues : un tableau d'objets avec au moins 'Date' et 'Quantité'
const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

// Computed pour générer l'option de graphique à partir des données
const chartOption = computed(() => ({
  title: {
    text: 'Quantité sur la période',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Quantité'],
    top: 30
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: props.data.map(item => item.Date)
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Quantité',
      type: 'line',
      smooth: true,
      data: props.data.map(item => Number(item.Quantité) || 0)
    }
  ]
}))
</script>


<!-- EChartsDashboard.vue -->
<template>
  <div class="echarts-dashboard">
    <!-- Header du composant -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ title }}</h2>
      <p class="text-gray-600">{{ description }}</p>
    </div>

    <!-- Container du graphique -->
    <div class="bg-white rounded-lg shadow-lg p-6">
      <!-- Loading state -->
      <div 
        v-if="isLoading" 
        class="flex items-center justify-center h-96"
      >
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Chargement du graphique...</span>
      </div>

      <!-- Graphique ECharts -->
      <div 
        ref="chartContainer"
        :id="chartId"
        class="w-full h-96 transition-opacity duration-300"
        :class="{ 'opacity-0': isLoading, 'opacity-100': !isLoading }"
      ></div>

      <!-- Actions -->
      <div class="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
        <div class="flex space-x-2">
          <button 
            @click="refreshChart"
            class="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors duration-200"
            :disabled="isLoading"
          >
            Actualiser
          </button>
          <button 
            @click="downloadChart"
            class="px-3 py-1 text-sm bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors duration-200"
            :disabled="isLoading"
          >
            Télécharger
          </button>
        </div>
        
        <div class="text-sm text-gray-500">
          Dernière mise à jour: {{ lastUpdate }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import * as echarts from 'echarts'

// Props
const props = defineProps({
  title: {
    type: String,
    default: 'Dashboard Analytics'
  },
  description: {
    type: String,
    default: 'Analyse des ventes par produit et évolution temporelle'
  },
  data: {
    type: Array,
    default: () => [
      ['product', '2012', '2013', '2014', '2015', '2016', '2017'],
      ['Milk Tea', 56.5, 82.1, 88.7, 70.1, 53.4, 85.1],
      ['Matcha Latte', 51.1, 51.4, 55.1, 53.3, 73.8, 68.7],
      ['Cheese Cocoa', 40.1, 62.2, 69.5, 36.4, 45.2, 32.5],
      ['Walnut Brownie', 25.2, 37.1, 41.2, 18, 33.9, 49.1]
    ]
  },
  height: {
    type: String,
    default: '400px'
  }
})

// Emits
const emit = defineEmits(['chart-ready', 'data-point-click'])

// Reactive data
const chartContainer = ref(null)
const myChart = ref(null)
const isLoading = ref(true)
const chartId = ref(`chart-${Date.now()}`)

// Computed
const lastUpdate = computed(() => {
  return new Date().toLocaleString('fr-FR')
})

// Configuration du graphique
const getChartOption = () => {
  return {
    legend: {
      top: 10,
      textStyle: {
        color: '#374151'
      }
    },
    tooltip: {
      trigger: 'axis',
      showContent: false,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      textStyle: {
        color: '#fff'
      }
    },
    dataset: {
      source: props.data
    },
    xAxis: { 
      type: 'category',
      axisLabel: {
        color: '#6B7280'
      },
      axisLine: {
        lineStyle: {
          color: '#E5E7EB'
        }
      }
    },
    yAxis: { 
      gridIndex: 0,
      axisLabel: {
        color: '#6B7280'
      },
      axisLine: {
        lineStyle: {
          color: '#E5E7EB'
        }
      },
      splitLine: {
        lineStyle: {
          color: '#F3F4F6'
        }
      }
    },
    grid: { 
      top: '55%',
      left: '10%',
      right: '10%',
      bottom: '10%'
    },
    series: [
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' },
        lineStyle: { width: 3 },
        symbolSize: 8
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' },
        lineStyle: { width: 3 },
        symbolSize: 8
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' },
        lineStyle: { width: 3 },
        symbolSize: 8
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' },
        lineStyle: { width: 3 },
        symbolSize: 8
      },
      {
        type: 'pie',
        id: 'pie',
        radius: '30%',
        center: ['50%', '25%'],
        emphasis: {
          focus: 'self',
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          formatter: '{b}: {@2012} ({d}%)',
          color: '#374151'
        },
        encode: {
          itemName: 'product',
          value: '2012',
          tooltip: '2012'
        }
      }
    ]
  }
}

// Méthodes
const initChart = async () => {
  if (!chartContainer.value) return

  try {
    isLoading.value = true
    
    // Attendre le prochain tick pour s'assurer que le DOM est rendu
    await nextTick()
    
    // Initialiser ECharts
    myChart.value = echarts.init(chartContainer.value)
    
    // Simuler un délai de chargement (optionnel)
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const option = getChartOption()
    
    // Event listener pour l'interaction pie/line
    myChart.value.on('updateAxisPointer', function (event) {
      const xAxisInfo = event.axesInfo[0]
      if (xAxisInfo) {
        const dimension = xAxisInfo.value + 1
        myChart.value.setOption({
          series: {
            id: 'pie',
            label: {
              formatter: '{b}: {@[' + dimension + ']} ({d}%)'
            },
            encode: {
              value: dimension,
              tooltip: dimension
            }
          }
        })
      }
    })
    
    // Event listener pour les clics
    myChart.value.on('click', (params) => {
      emit('data-point-click', params)
    })
    
    // Appliquer les options
    myChart.value.setOption(option)
    
    isLoading.value = false
    emit('chart-ready', myChart.value)
    
  } catch (error) {
    console.error('Erreur lors de l\'initialisation du graphique:', error)
    isLoading.value = false
  }
}

const refreshChart = async () => {
  if (myChart.value) {
    myChart.value.dispose()
  }
  await initChart()
}

const downloadChart = () => {
  if (myChart.value) {
    const url = myChart.value.getDataURL({
      type: 'png',
      pixelRatio: 2,
      backgroundColor: '#fff'
    })
    
    const link = document.createElement('a')
    link.download = `dashboard-${Date.now()}.png`
    link.href = url
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

const resizeChart = () => {
  if (myChart.value) {
    myChart.value.resize()
  }
}

// Watchers
watch(() => props.data, () => {
  if (myChart.value) {
    const option = getChartOption()
    myChart.value.setOption(option)
  }
}, { deep: true })

// Lifecycle hooks
onMounted(async () => {
  await initChart()
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeChart)
  if (myChart.value) {
    myChart.value.dispose()
  }
})
</script>

<style scoped>
.echarts-dashboard {
  @apply w-full;
}

/* Animation pour le loading */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>

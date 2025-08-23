<template>
  <div class="w-full">
    <!-- État de chargement -->
    <div v-if="loading" class="flex justify-center items-center h-96">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p class="text-gray-600 text-lg">Chargement des données...</p>
      </div>
    </div>
    
    <!-- Affichage d'erreur -->
    <div v-else-if="error" class="flex flex-col justify-center items-center h-96 bg-red-50 rounded-lg border border-red-200">
      <div class="text-center p-6">
        <svg class="mx-auto h-12 w-12 text-red-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-lg font-medium text-red-900 mb-2">Erreur de chargement</h3>
        <p class="text-red-700 mb-4">{{ error }}</p>
        <button 
          @click="loadData" 
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
        >
          <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Réessayer
        </button>
      </div>
    </div>
    
    <!-- Graphique -->
    <div v-else-if="sheetData.length > 0" class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div class="mb-4 text-center">
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ subtitle }}</p>
      </div>
      
      <v-chart 
        :option="chartOption" 
        :style="{ width: chartWidth, height: chartHeight }"
        class="mx-auto"
        @click="onChartClick"
      />
      
      <!-- Légende personnalisée (optionnelle) -->
      <div v-if="showCustomLegend" class="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div 
          v-for="(item, index) in legendData" 
          :key="index"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex items-center">
            <div 
              class="w-4 h-4 rounded-full mr-3 flex-shrink-0"
              :style="{ backgroundColor: getColor(index) }"
            ></div>
            <span class="font-medium text-gray-900">{{ item.name }}</span>
          </div>
          <span class="text-sm font-semibold text-gray-700">
            {{ new Intl.NumberFormat('fr-FR').format(item.value) }}€
          </span>
        </div>
      </div>
    </div>
    
    <!-- Aucune donnée -->
    <div v-else class="flex flex-col justify-center items-center h-96 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
      <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H9z" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-1">Aucune donnée</h3>
      <p class="text-gray-500">Les données ne sont pas disponibles pour le moment.</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { useSheet } from '@/composables/useSheet'

// Import des modules nécessaires pour pie chart
import { PieChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { 
  GridComponent, 
  TooltipComponent, 
  LegendComponent, 
  TitleComponent 
} from 'echarts/components'

// Enregistre les modules auprès de echarts
use([PieChart, CanvasRenderer, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

// Props
const props = defineProps({
  docName: {
    type: String,
    default: 'overfolio'
  },
  title: {
    type: String,
    default: 'Répartition des données'
  },
  subtitle: {
    type: String,
    default: ''
  },
  chartWidth: {
    type: String,
    default: '100%'
  },
  chartHeight: {
    type: String,
    default: '400px'
  },
  padAngle: {
    type: Number,
    default: 0.02 // Espace entre les secteurs
  },
  showCustomLegend: {
    type: Boolean,
    default: false
  },
  labelField: {
    type: String,
    default: 'Actif' // Champ pour les labels (crypto, fiat, stock, etc.)
  },
  valueField: {
    type: String,
    default: 'Assets' // Champ pour les valeurs
  },
  colors: {
    type: Array,
    default: () => [
      '#5470c6', '#91cc75', '#fac858', '#ee6666', 
      '#73c0de', '#3ba272', '#fc8452', '#9a60b4', 
      '#ea7ccc', '#8d4653', '#d48265', '#61a0a8'
    ]
  }
})

// Émissions
const emit = defineEmits(['chart-click', 'data-loaded'])

// Utilisation du composable
const { sheetData, loading, error, getSheetData } = useSheet()

// Fonction pour charger les données
const loadData = async () => {
  try {
    await getSheetData(props.docName)
    emit('data-loaded', sheetData.value)
  } catch (err) {
    console.error('Erreur lors du chargement:', err)
  }
}

// Données formatées pour la légende avec agrégation par Actif
const legendData = computed(() => {
  const aggregatedData = aggregateDataByActif.value
  return aggregatedData.map(item => ({
    name: item.name,
    value: item.value
  }))
})

// Agrégation des données par type d'actif
const aggregateDataByActif = computed(() => {
  const grouped = {}
  
  sheetData.value.forEach(item => {
    const actif = item[props.labelField] || 'Autre'
    const assets = Number(item[props.valueField]) || 0
    
    // Ignorer les valeurs négatives et nulles pour le pie chart
    if (assets > 0) {
      if (!grouped[actif]) {
        grouped[actif] = 0
      }
      grouped[actif] += assets
    }
  })
  
  return Object.entries(grouped)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value) // Trier par valeur décroissante
})

// Fonction pour obtenir la couleur d'un index
const getColor = (index) => {
  return props.colors[index % props.colors.length]
}

// Gestion du clic sur le graphique
const onChartClick = (params) => {
  emit('chart-click', params)
}

// Configuration du graphique pie
const chartOption = computed(() => {
  const data = aggregateDataByActif.value.map((item, index) => ({
    name: item.name,
    value: item.value,
    itemStyle: {
      color: getColor(index)
    }
  }))

  // Calculer le total pour les pourcentages
  const total = data.reduce((sum, item) => sum + item.value, 0)

  return {
    title: {
      text: props.title,
      left: 'center',
      top: '5%',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#1f2937'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const percent = params.percent
        const value = params.value
        const name = params.name
        // Format des nombres avec séparateurs de milliers
        const formattedValue = new Intl.NumberFormat('fr-FR').format(value)
        return `
          <div class="font-semibold">${name}</div>
          <div class="text-sm">
            <span class="inline-block w-3 h-3 rounded-full mr-1" style="background-color: ${params.color}"></span>
            Valeur: <span class="font-medium">${formattedValue} €</span>
          </div>
          <div class="text-sm">Pourcentage: <span class="font-medium">${percent}%</span></div>
        `
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: {
        color: '#374151'
      }
    },
    legend: {
      show: !props.showCustomLegend,
      type: 'scroll',
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      itemWidth: 14,
      itemHeight: 14,
      textStyle: {
        fontSize: 12,
        color: '#6b7280'
      },
      formatter: function(name) {
        const item = data.find(d => d.name === name)
        const formattedValue = new Intl.NumberFormat('fr-FR', { 
          maximumFractionDigits: 0 
        }).format(item ? item.value : 0)
        return `${name} (${formattedValue}€)`
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'], // Donut chart
        center: ['50%', '50%'],
        padAngle: props.padAngle,
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: function(params) {
            const formattedValue = new Intl.NumberFormat('fr-FR', { 
              maximumFractionDigits: 0 
            }).format(params.value)
            return `${params.name}\n${params.percent}%\n(${formattedValue}€)`
          },
          fontSize: 11,
          color: '#4b5563'
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 10,
          smooth: true
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          },
          label: {
            fontSize: 14,
            fontWeight: 'bold'
          }
        },
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: function (idx) {
          return Math.random() * 200
        },
        data: data
      }
    ]
  }
})

// Chargement au montage du composant
onMounted(() => {
  loadData()
})

// Exposer les fonctions utiles
defineExpose({
  loadData,
  sheetData,
  legendData,
  aggregateDataByActif
})
</script>

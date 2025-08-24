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
    
    <!-- Graphique Rose -->
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
      
      <!-- Statistiques résumées -->
      <div class="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="text-center p-3 bg-gray-50 rounded-lg">
          <div class="text-2xl font-bold text-blue-600">{{ aggregateDataByActif.length }}</div>
          <div class="text-sm text-gray-600">Types d'actifs</div>
        </div>
        <div class="text-center p-3 bg-gray-50 rounded-lg">
          <div class="text-2xl font-bold text-green-600">
            {{ new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 }).format(totalValue) }}€
          </div>
          <div class="text-sm text-gray-600">Valeur totale</div>
        </div>
        <div class="text-center p-3 bg-gray-50 rounded-lg">
          <div class="text-2xl font-bold text-purple-600">{{ topAsset.name }}</div>
          <div class="text-sm text-gray-600">Plus gros actif</div>
        </div>
        <div class="text-center p-3 bg-gray-50 rounded-lg">
          <div class="text-2xl font-bold text-orange-600">
            {{ Math.round(topAsset.percentage) }}%
          </div>
          <div class="text-sm text-gray-600">Part principale</div>
        </div>
      </div>
      
      <!-- Légende détaillée -->
      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div 
          v-for="(item, index) in legendData" 
          :key="index"
          class="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border hover:shadow-md transition-shadow cursor-pointer"
          @click="highlightSector(item.name)"
        >
          <div class="flex items-center">
            <div 
              class="w-5 h-5 rounded-full mr-3 flex-shrink-0 shadow-sm"
              :style="{ backgroundColor: getColor(index) }"
            ></div>
            <div>
              <div class="font-medium text-gray-900">{{ item.name }}</div>
              <div class="text-sm text-gray-600">
                {{ Math.round((item.value / totalValue) * 100) }}% du total
              </div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-lg font-semibold text-gray-900">
              {{ new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 }).format(item.value) }}€
            </div>
            <div class="text-sm text-gray-500">
              {{ getAssetTypeLabel(item.name) }}
            </div>
          </div>
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
    default: 'Répartition des actifs en rose'
  },
  subtitle: {
    type: String,
    default: 'Visualisation en pétales selon la valeur'
  },
  chartWidth: {
    type: String,
    default: '100%'
  },
  chartHeight: {
    type: String,
    default: '500px'
  },
  roseType: {
    type: String,
    default: 'radius', // 'radius' ou 'area'
    validator: (value) => ['radius', 'area'].includes(value)
  },
  labelField: {
    type: String,
    default: 'Actif'
  },
  valueField: {
    type: String,
    default: 'Equity'
  },
  colors: {
    type: Array,
    default: () => [
      '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', 
      '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd',
      '#00d2d3', '#ff9f43', '#10ac84', '#ee5a24'
    ]
  }
})

// Émissions
const emit = defineEmits(['chart-click', 'data-loaded', 'sector-highlight'])

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

// Agrégation des données par type d'actif
const aggregateDataByActif = computed(() => {
  const grouped = {}
  
  sheetData.value.forEach(item => {
    const actif = item[props.labelField] || 'Autre'
    const assets = Number(item[props.valueField]) || 0
    
    if (assets > 0) {
      if (!grouped[actif]) {
        grouped[actif] = 0
      }
      grouped[actif] += assets
    }
  })
  
  return Object.entries(grouped)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value)
})

// Données formatées pour la légende
const legendData = computed(() => {
  return aggregateDataByActif.value.map(item => ({
    name: item.name,
    value: item.value
  }))
})

// Valeur totale
const totalValue = computed(() => {
  return aggregateDataByActif.value.reduce((sum, item) => sum + item.value, 0)
})

// Plus gros actif
const topAsset = computed(() => {
  if (aggregateDataByActif.value.length === 0) {
    return { name: '-', percentage: 0 }
  }
  const top = aggregateDataByActif.value[0]
  return {
    name: top.name,
    percentage: (top.value / totalValue.value) * 100
  }
})

// Fonction pour obtenir la couleur d'un index
const getColor = (index) => {
  return props.colors[index % props.colors.length]
}

// Labels pour les types d'actifs
const getAssetTypeLabel = (actif) => {
  const labels = {
    'crypto': 'Cryptomonnaies',
    'fiat': 'Liquidités',
    'stock': 'Actions',
    'immobilier': 'Immobilier',
    'commodity': 'Matières premières'
  }
  return labels[actif] || actif
}

// Gestion du clic sur le graphique
const onChartClick = (params) => {
  emit('chart-click', params)
}

// Fonction pour mettre en évidence un secteur
const highlightSector = (sectorName) => {
  emit('sector-highlight', sectorName)
}

// Configuration du graphique rose
const chartOption = computed(() => {
  const data = aggregateDataByActif.value.map((item, index) => ({
    name: item.name,
    value: item.value,
    itemStyle: {
      color: getColor(index),
      borderRadius: 3,
      borderColor: '#fff',
      borderWidth: 1
    }
  }))

  return {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const percent = params.percent
        const value = params.value
        const name = params.name
        const formattedValue = new Intl.NumberFormat('fr-FR').format(value)
        return `
          <div class="font-semibold text-lg mb-2">${getAssetTypeLabel(name)}</div>
          <div class="text-sm mb-1">
            <span class="inline-block w-3 h-3 rounded-full mr-2" style="background-color: ${params.color}"></span>
            Valeur: <span class="font-bold">${formattedValue} €</span>
          </div>
          <div class="text-sm mb-1">Part: <span class="font-bold">${percent}%</span></div>
          <div class="text-xs text-gray-500">Cliquez pour plus de détails</div>
        `
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: {
        color: '#374151'
      },
      extraCssText: 'border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'
    },
    legend: {
      show: false // On utilise notre légende personnalisée
    },
    series: [
      {
        type: 'pie',
        radius: ['30%', '75%'],
        center: ['50%', '50%'],
        roseType: props.roseType, // 'radius' ou 'area'
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: function(params) {
            if (params.percent < 5) return '' // Masquer les labels des petits secteurs
            return `${params.name}\n${params.percent}%`
          },
          fontSize: 12,
          fontWeight: 'bold',
          color: '#374151'
        },
        labelLine: {
          show: true,
          length: 20,
          length2: 10,
          smooth: true
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 20,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.3)',
            scale: 1.1
          },
          label: {
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: function (idx) {
          return idx * 100
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
  aggregateDataByActif,
  totalValue,
  topAsset
})
</script>

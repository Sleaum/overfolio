<template>
  <div>
    <!-- État de chargement -->
    <div v-if="loading" class="loading">
      Chargement des données...
    </div>
    
    <!-- Affichage d'erreur -->
    <div v-else-if="error" class="error">
      Erreur: {{ error }}
      <button @click="loadData" class="retry-btn">Réessayer</button>
    </div>
    
    <!-- Graphique -->
    <v-chart 
      v-else-if="sheetData.length > 0" 
      :option="chartOption" 
      style="width: 600px; height: 400px;" 
    />
    
    <!-- Aucune donnée -->
    <div v-else class="no-data">
      Aucune donnée disponible
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { useSheet } from '@/composables/useSheet'

// Import des modules nécessaires (modulaire pour echarts 5)
import { LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent } from 'echarts/components'

// Enregistre les modules auprès de echarts
use([LineChart, CanvasRenderer, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

// Props
const props = defineProps({
  docName: {
    type: String,
    default: 'overfolio'
  }
})

// Utilisation du composable
const { sheetData, loading, error, getSheetData } = useSheet()

// Fonction pour charger les données
const loadData = async () => {
  try {
    await getSheetData(props.docName)
  } catch (err) {
    // L'erreur est déjà gérée dans le composable
    console.error('Erreur lors du chargement:', err)
  }
}

// Computed pour générer l'option de graphique
const chartOption = computed(() => ({
  title: {
    text: 'Quantité sur la période',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis',
    formatter: function (params) {
      if (params.length > 0) {
        const dataIndex = params[0].dataIndex
        const item = sheetData.value[dataIndex]
        return `Date: ${item.Date}<br/>Quantité: ${item.Quantité}`
      }
      return ''
    }
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
    data: sheetData.value.map(item => item.Date),
    axisLabel: {
      rotate: 45
    }
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Quantité',
      type: 'line',
      smooth: true,
      data: sheetData.value.map(item => Number(item.Quantité) || 0),
      itemStyle: {
        color: '#5470c6'
      },
      areaStyle: {
        opacity: 0.1
      }
    }
  ]
}))

// Chargement au montage du composant
onMounted(() => {
  loadData()
})

// Exposer les fonctions utiles
defineExpose({
  loadData,
  sheetData
})
</script>

<style scoped>
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  font-size: 16px;
  color: #666;
}

.error {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 400px;
  color: #d32f2f;
  font-size: 16px;
  text-align: center;
  gap: 16px;
}

.retry-btn {
  padding: 8px 16px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background: #1565c0;
}

.no-data {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  color: #666;
  font-size: 16px;
}
</style>

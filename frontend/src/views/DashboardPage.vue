<!-- DashboardPage.vue -->
<template>
  <div class="dashboard-page min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4">
      <!-- Header de la page -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Tableau de Bord</h1>
        <p class="text-gray-600">Analyse des performances de vente</p>
      </div>

      <!-- Grille de composants -->
      <div class="grid grid-cols-1 xl:grid-cols-2 gap-8">
        
        <!-- Graphique principal -->
        <div class="xl:col-span-2">
          <EChartsDashboard
            :data="salesData"
            title="Évolution des Ventes par Produit"
            description="Analyse temporelle avec vue d'ensemble circulaire interactive"
            @chart-ready="onChartReady"
            @data-point-click="onDataPointClick"
          />
        </div>

        <!-- Graphique secondaire avec données différentes -->
        <EChartsDashboard
          :data="revenueData"
          title="Revenus Trimestriels"
          description="Comparaison des revenus par trimestre"
          @chart-ready="onSecondChartReady"
        />

        <!-- Statistiques rapides -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h3 class="text-xl font-bold text-gray-800 mb-4">Statistiques Clés</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-2xl font-bold text-blue-600">{{ totalSales }}</div>
              <div class="text-sm text-gray-600">Ventes Totales</div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-2xl font-bold text-green-600">{{ bestProduct }}</div>
              <div class="text-sm text-gray-600">Meilleur Produit</div>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg">
              <div class="text-2xl font-bold text-purple-600">{{ growthRate }}%</div>
              <div class="text-sm text-gray-600">Croissance</div>
            </div>
            <div class="text-center p-4 bg-orange-50 rounded-lg">
              <div class="text-2xl font-bold text-orange-600">{{ avgSales }}</div>
              <div class="text-sm text-gray-600">Moyenne</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions globales -->
      <div class="mt-8 flex justify-center space-x-4">
        <button 
          @click="refreshAllData"
          class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200"
        >
          Actualiser toutes les données
        </button>
        <button 
          @click="exportData"
          class="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors duration-200"
        >
          Exporter les données
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import EChartsDashboard from '@/components/EChartsDashboard.vue'

// Reactive data
const salesData = ref([
  ['product', '2012', '2013', '2014', '2015', '2016', '2017'],
  ['Milk Tea', 56.5, 82.1, 88.7, 70.1, 53.4, 85.1],
  ['Matcha Latte', 51.1, 51.4, 55.1, 53.3, 73.8, 68.7],
  ['Cheese Cocoa', 40.1, 62.2, 69.5, 36.4, 45.2, 32.5],
  ['Walnut Brownie', 25.2, 37.1, 41.2, 18, 33.9, 49.1]
])

const revenueData = ref([
  ['quarter', 'Q1', 'Q2', 'Q3', 'Q4'],
  ['Revenus', 1200, 1450, 1800, 1650],
  ['Coûts', 800, 900, 1200, 1100],
  ['Profit', 400, 550, 600, 550]
])

// Computed properties
const totalSales = computed(() => {
  let total = 0
  salesData.value.slice(1).forEach(row => {
    row.slice(1).forEach(value => {
      total += value
    })
  })
  return Math.round(total)
})

const bestProduct = computed(() => {
  let maxTotal = 0
  let bestProd = ''
  
  salesData.value.slice(1).forEach(row => {
    const total = row.slice(1).reduce((sum, val) => sum + val, 0)
    if (total > maxTotal) {
      maxTotal = total
      bestProd = row[0]
    }
  })
  
  return bestProd
})

const growthRate = computed(() => {
  // Calcul simplifié du taux de croissance
  return 15.3
})

const avgSales = computed(() => {
  const total = totalSales.value
  const count = salesData.value.length - 1 // -1 pour exclure l'header
  const years = salesData.value[0].length - 1 // -1 pour exclure 'product'
  return Math.round(total / (count * years))
})

// Methods
const onChartReady = (chartInstance) => {
  console.log('Graphique principal prêt:', chartInstance)
}

const onSecondChartReady = (chartInstance) => {
  console.log('Graphique secondaire prêt:', chartInstance)
}

const onDataPointClick = (params) => {
  console.log('Point de données cliqué:', params)
  // Ici vous pourriez ouvrir un modal avec plus de détails
  alert(`Clicked on: ${params.name} - Value: ${params.value}`)
}

const refreshAllData = async () => {
  // Simuler un appel API
  console.log('Actualisation des données...')
  
  // Exemple de mise à jour des données
  setTimeout(() => {
    // Modifier légèrement les données pour simuler une mise à jour
    salesData.value = salesData.value.map((row, index) => {
      if (index === 0) return row // Garder l'header
      return [
        row[0], // Garder le nom du produit
        ...row.slice(1).map(val => val + (Math.random() - 0.5) * 10)
      ]
    })
    console.log('Données actualisées')
  }, 1000)
}

const exportData = () => {
  // Créer un CSV simple
  const csvContent = salesData.value
    .map(row => row.join(','))
    .join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `sales-data-${Date.now()}.csv`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  window.URL.revokeObjectURL(url)
}

// Lifecycle
onMounted(() => {
  console.log('Dashboard page mounted')
})
</script>

<style scoped>
.dashboard-page {
  /* Styles additionnels si nécessaire */
}
</style>

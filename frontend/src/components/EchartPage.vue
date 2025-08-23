<template>
    <VueEChartsComponent 
      doc-name="overfolio" 
      api-url="http://localhost:8000/api/sheet" 
    />
    <PieChartComponent
      doc-name="overfolio"
      title="Répartition du portefeuille par type d'actif"
      subtitle="Données au 23 août 2025"
      :pad-angle="0.02"
      chart-height="500px"
      :show-custom-legend="true"
      :colors="['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']"
      @chart-click="handleAssetClick"
    />
</template>

<script setup>
import VueEChartsComponent from './VueEChartsComponent.vue'
import PieChartComponent from './PiePadangleComponent.vue'
</script>

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
    <RoseChartComponent
      doc-name="overfolio"
      title="Portfolio en Rose - Area"
      subtitle="Surface proportionnelle à la valeur"
      rose-type="area"
      chart-height="600px"
      :colors="['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']"
    />
</template>

<script setup>
import VueEChartsComponent from '../components/VueEChartsComponent.vue'
import PieChartComponent from '../components/PiePadangleComponent.vue'
import RoseChartComponent from '../components/PieRose.vue'
</script>

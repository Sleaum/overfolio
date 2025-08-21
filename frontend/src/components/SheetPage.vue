<template>
  <div>
    <h2>Données du jour</h2>
    <table v-if="data.length">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td v-for="(value, key) in row" :key="key">{{ value }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Aucune donnée disponible</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

// Génère dynamiquement les en-têtes de colonnes à partir des clés du premier objet
const headers = computed(() => (props.data.length ? Object.keys(props.data[0]) : []))
</script>


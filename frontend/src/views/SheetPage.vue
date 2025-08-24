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
import { ref, computed, onMounted } from 'vue'

// état local
const data = ref([])

// headers calculés automatiquement
const headers = computed(() =>
  data.value.length ? Object.keys(data.value[0]) : []
)

// récupération des données au montage
onMounted(async () => {
  try {
    const response = await fetch('http://localhost/api/sheet?doc_name=overfolio')
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des données')
    }
    const json = await response.json()
    data.value = json
  } catch (error) {
    console.error(error)
  }
})
</script>


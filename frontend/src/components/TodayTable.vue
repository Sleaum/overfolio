<template>
  <div>
    <h2>Données du jour</h2>
    <table v-if="todayData.length">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in todayData" :key="index">
          <td v-for="(value, key) in row" :key="key">{{ value }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Aucune donnée disponible</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const todayData = ref([]);
const headers = ref([]);

onMounted(async () => {
  try {
    const res = await fetch('/api/googlesheet/?doc_name=overfolio');
    const data = await res.json();
    todayData.value = data.today;
    if (data.today.length) {
      headers.value = Object.keys(data.today[0]);
    }
  } catch (err) {
    console.error('Erreur de fetch:', err);
  }
});
</script>


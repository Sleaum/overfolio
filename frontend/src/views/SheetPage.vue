<template>
  <section class="sheet-page">
    <header class="sheet-header">
      <h2>Données du jour</h2>
      <button type="button" class="refresh" :disabled="loading" @click="load(true)">
        {{ loading ? 'Chargement…' : 'Actualiser' }}
      </button>
    </header>

    <p v-if="error" class="state state-error" role="alert">Erreur : {{ error }}</p>
    <p v-else-if="loading && !rows.length" class="state">Chargement des données…</p>
    <p v-else-if="!rows.length" class="state">Aucune donnée disponible</p>

    <div v-if="rows.length" class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th v-for="header in headers" :key="header" scope="col">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in rows" :key="index">
            <td
              v-for="header in headers"
              :key="header"
              :class="{ num: typeof row[header] === 'number' }"
            >
              {{ row[header] ?? '' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useSheet } from '@/composables/useSheet'

const props = defineProps({
  docName: { type: String, default: 'overfolio' },
  sheetName: { type: String, default: '' },
})

const { sheetData: rows, loading, error, getSheetData } = useSheet()

// Colonnes = union des clés de toutes les lignes, dans l'ordre d'apparition
const headers = computed(() => {
  const columns = new Set()
  for (const row of rows.value) {
    for (const key of Object.keys(row)) columns.add(key)
  }
  return [...columns]
})

const load = async (refresh = false) => {
  try {
    await getSheetData(props.docName, { sheetName: props.sheetName, refresh })
  } catch {
    // le message est affiché grâce à la variable `error`
  }
}

onMounted(() => load())
</script>

<style scoped>
.sheet-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.sheet-header h2 {
  margin: 0;
}

.refresh {
  padding: 0.45rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
}

.refresh:disabled {
  opacity: 0.6;
  cursor: default;
}

.state {
  padding: 1rem;
  text-align: center;
  color: #475569;
}

.state-error {
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
}

.table-wrapper {
  overflow: auto;
  max-height: 70vh;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

th,
td {
  padding: 0.55rem 0.85rem;
  text-align: left;
  white-space: nowrap;
  border-bottom: 1px solid #e2e8f0;
}

thead th {
  position: sticky;
  top: 0;
  background: #f1f5f9;
  font-weight: 600;
}

tbody tr:nth-child(even) {
  background: #f8fafc;
}

tbody tr:hover {
  background: #eef2ff;
}

td.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
</style>

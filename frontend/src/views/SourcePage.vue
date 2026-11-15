<template>
  <section class="source-page">
    <header class="page-header">
      <h2>Source des données</h2>
      <div class="picker">
        <label for="table-select">Table</label>
        <select id="table-select" v-model="selected" :disabled="!tables.length">
          <option v-for="table in tables" :key="table.name" :value="table.name">
            {{ table.name }} ({{ table.row_count }} lignes)
          </option>
        </select>
      </div>
    </header>

    <p v-if="error" class="state state-error" role="alert">Erreur : {{ error }}</p>
    <p v-else-if="loadingTables" class="state">Chargement des tables…</p>
    <p v-else-if="!tables.length" class="state">
      Aucune table en base. Lance <code>python manage.py sync_sheets</code> pour la remplir.
    </p>

    <template v-else-if="current">
      <div class="toolbar">
        <p class="meta">
          {{ filteredRows.length }} ligne(s) sur {{ current.row_count }}
          <span v-if="current.synced_at"> · synchronisé le {{ syncedAt }}</span>
        </p>
        <input
          v-model="query"
          type="search"
          class="search"
          placeholder="Rechercher dans la table…"
          aria-label="Rechercher dans la table"
        />
      </div>

      <p v-if="!filteredRows.length" class="state">Aucune ligne ne correspond.</p>

      <div v-else class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th v-for="column in current.columns" :key="column" scope="col">{{ column }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in pagedRows" :key="index">
              <td
                v-for="column in current.columns"
                :key="column"
                :class="{ num: typeof row[column] === 'number' }"
              >
                {{ row[column] ?? '' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <nav v-if="totalPages > 1" class="pager" aria-label="Pagination">
        <button type="button" :disabled="page <= 1" @click="page--">Précédent</button>
        <span>Page {{ page }} / {{ totalPages }}</span>
        <button type="button" :disabled="page >= totalPages" @click="page++">Suivant</button>
      </nav>
    </template>

    <p v-else-if="loadingData" class="state">Chargement de la table…</p>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const PAGE_SIZE = 50

const tables = ref([])
const selected = ref('')
const current = ref(null)
const loadingTables = ref(false)
const loadingData = ref(false)
const error = ref(null)
const query = ref('')
const page = ref(1)

async function getJson(url) {
  const response = await fetch(url, { headers: { Accept: 'application/json' } })
  if (!response.ok) {
    let message = `Erreur HTTP ${response.status}`
    try {
      const body = await response.json()
      if (body?.error) message = body.error
    } catch {
      // corps non JSON : on garde le code HTTP
    }
    throw new Error(message)
  }
  return response.json()
}

// Évite qu'une réponse lente écrase celle de la table choisie ensuite
let requestId = 0

async function loadTable(name) {
  const id = ++requestId
  loadingData.value = true
  error.value = null
  try {
    const data = await getJson(`/api/data/${encodeURIComponent(name)}/`)
    if (id === requestId) current.value = data
  } catch (err) {
    if (id === requestId) {
      current.value = null
      error.value = err.message
    }
  } finally {
    if (id === requestId) loadingData.value = false
  }
}

onMounted(async () => {
  loadingTables.value = true
  try {
    tables.value = await getJson('/api/data/')
    if (tables.value.length) selected.value = tables.value[0].name
  } catch (err) {
    error.value = err.message
  } finally {
    loadingTables.value = false
  }
})

watch(selected, (name) => {
  query.value = ''
  page.value = 1
  if (name) loadTable(name)
})

watch(query, () => {
  page.value = 1
})

const filteredRows = computed(() => {
  const rows = current.value?.rows ?? []
  const needle = query.value.trim().toLowerCase()
  if (!needle) return rows
  const columns = current.value.columns
  return rows.filter((row) =>
    columns.some((column) => String(row[column] ?? '').toLowerCase().includes(needle)),
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredRows.value.length / PAGE_SIZE)))

const pagedRows = computed(() => {
  const start = (Math.min(page.value, totalPages.value) - 1) * PAGE_SIZE
  return filteredRows.value.slice(start, start + PAGE_SIZE)
})

const syncedAt = computed(() =>
  current.value?.synced_at ? new Date(current.value.synced_at).toLocaleString('fr-FR') : '',
)
</script>

<style scoped>
.source-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

.page-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.page-header h2 {
  margin: 0;
}

.picker {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.picker select,
.search {
  padding: 0.45rem 0.7rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #fff;
  font-size: 0.95rem;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.meta {
  margin: 0;
  color: #475569;
  font-size: 0.9rem;
}

.search {
  min-width: 240px;
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
  font-size: 0.9rem;
}

th,
td {
  padding: 0.5rem 0.8rem;
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

.pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.pager button {
  padding: 0.4rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
}

.pager button:disabled {
  opacity: 0.5;
  cursor: default;
}
</style>

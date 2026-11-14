 // composables/useSheet.js
import { ref } from 'vue'

 // Extrait le message d'erreur renvoyé par le backend ({ "error": "..." })
async function readErrorMessage(response) {
  try {
    const body = await response.json()
    if (body?.error) return body.error
    if (body?.detail) return body.detail
  } catch {
    // corps non JSON : on retombe sur le code HTTP
  }
  const statusText = response.statusText ? ` - ${response.statusText}` : ''
  return `Erreur HTTP ${response.status}${statusText}`
}

 // Composable pour les appels API génériques
function useApi() {
  const loading = ref(false)
  const error = ref(null)

  // URL relative par défaut : nginx redirige /api/ vers Django
  const baseURL = import.meta.env.VITE_API_URL || ''

  const fetchData = async (endpoint, options = {}) => {
    loading.value = true
    error.value = null
    try {
      const url = endpoint.startsWith('http') ? endpoint : `${baseURL}${endpoint}`
      const { headers, ...rest } = options

      const response = await fetch(url, {
        ...rest,
        headers: {
          Accept: 'application/json',
          ...(rest.body ? { 'Content-Type': 'application/json' } : {}),
          ...headers,
        },
      })

      if (!response.ok) {
        throw new Error(await readErrorMessage(response))
      }

      return await response.json()
    } catch (err) {
      error.value = err.message
      console.error('Erreur API:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return { loading, error, fetchData }
}

// Composable spécialisé pour les Google Sheets
export function useSheet() {
  const { loading, error, fetchData } = useApi()
  const sheetData = ref([])

  // getSheetData('overfolio')
  // getSheetData('overfolio', { sheetName: 'Janvier', refresh: true })
  const getSheetData = async (docName, { sheetName = '', refresh = false } = {}) => {
    const params = new URLSearchParams({ doc_name: docName })
    if (sheetName) params.set('sheet_name', sheetName)
    if (refresh) params.set('refresh', '1')

    const data = await fetchData(`/api/sheet?${params}`)

    if (!Array.isArray(data)) {
      const message = 'Format de données incorrect : un tableau est attendu'
      error.value = message
      throw new Error(message)
    }

    sheetData.value = data
    return data
  }

  return { sheetData, loading, error, getSheetData }
}

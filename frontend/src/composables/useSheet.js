// composables/useSheet.js
import { ref } from 'vue'

// Composable pour les appels API génériques
function useApi() {
  const loading = ref(false)
  const error = ref(null)
  
  // Configuration de base - utilise l'URL relative pour le proxy
  const baseURL = import.meta.env.VITE_API_URL || ''
  
  const fetchData = async (endpoint, options = {}) => {
    try {
      loading.value = true
      error.value = null
      
      const url = endpoint.startsWith('http') ? endpoint : `${baseURL}${endpoint}`
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })
      
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status} - ${response.statusText}`)
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
  
  return {
    loading,
    error,
    fetchData
  }
}

// Composable spécialisé pour les sheets
export function useSheet() {
  const { loading, error, fetchData } = useApi()
  const sheetData = ref([])
  
  const getSheetData = async (docName) => {
    try {
      const data = await fetchData(`/api/sheet?doc_name=${docName}`)
      
      if (Array.isArray(data)) {
        sheetData.value = data
      } else {
        throw new Error('Format de données incorrect: attendu un tableau')
      }
      
      return data
    } catch (err) {
      sheetData.value = []
      throw err
    }
  }
  
  return {
    sheetData,
    loading,
    error,
    getSheetData
  }
}

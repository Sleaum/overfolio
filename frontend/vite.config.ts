import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { fileURLToPath } from 'url'

// Remplace __dirname en mode ES module
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
    
export default defineConfig({
  plugins: [vue()],        
  resolve: {               
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: '0.0.0.0',       
    port: 5173,
    // Configuration du proxy pour éviter les erreurs CORS
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Votre serveur Django
        changeOrigin: true,
        secure: false
      }
    }
  } 
})

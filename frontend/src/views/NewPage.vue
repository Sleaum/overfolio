<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center p-4">
    <!-- Particules de fond animées -->
    <div class="absolute inset-0 overflow-hidden">
      <div v-for="i in 50" :key="i" 
           class="absolute w-2 h-2 bg-white rounded-full opacity-20 animate-pulse"
           :style="{
             left: Math.random() * 100 + '%',
             top: Math.random() * 100 + '%',
             animationDelay: Math.random() * 2 + 's',
             animationDuration: (Math.random() * 3 + 2) + 's'
           }">
      </div>
    </div>

    <!-- Container principal -->
    <div class="relative w-full max-w-md">
      <!-- Carte de connexion -->
      <div class="bg-white/10 backdrop-blur-lg rounded-3xl shadow-2xl border border-white/20 p-8 transform hover:scale-105 transition-all duration-300">
        <!-- Logo/Titre -->
        <div class="text-center mb-8">
          <div class="w-20 h-20 bg-gradient-to-tr from-blue-400 to-purple-500 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center">
              <div class="w-6 h-6 bg-gradient-to-tr from-blue-500 to-purple-600 rounded"></div>
            </div>
          </div>
          <h1 class="text-3xl font-bold text-white mb-2">Connexion</h1>
          <p class="text-white/70">Accédez à votre espace personnel</p>
        </div>

        <!-- Formulaire -->
        <div class="space-y-6">
          <!-- Champ Email -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 7.89a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
            <input
              v-model="email"
              type="email"
              placeholder="Adresse email"
              required
              class="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent backdrop-blur-sm transition-all duration-300"
            />
          </div>

          <!-- Champ Mot de passe -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Mot de passe"
              required
              class="w-full pl-10 pr-12 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent backdrop-blur-sm transition-all duration-300"
            />
            <button
              type="button"
              @click="togglePasswordVisibility"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-white/50 hover:text-white transition-colors"
            >
              <svg v-if="!showPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
              </svg>
            </button>
          </div>

          <!-- Options -->
          <div class="flex items-center justify-between">
            <label class="flex items-center cursor-pointer">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="sr-only"
              />
              <div class="relative">
                <div class="w-5 h-5 bg-white/10 border border-white/20 rounded transition-all duration-200"
                     :class="{ 'bg-blue-500 border-blue-500': rememberMe }">
                  <div v-if="rememberMe" class="absolute inset-0 flex items-center justify-center">
                    <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                  </div>
                </div>
              </div>
              <span class="ml-2 text-white/70 text-sm">Se souvenir de moi</span>
            </label>
            <a href="#" class="text-blue-300 hover:text-blue-200 text-sm transition-colors">
              Mot de passe oublié ?
            </a>
          </div>

          <!-- Bouton de connexion -->
          <button
            @click="handleLogin"
            :disabled="isLoading"
            class="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-lg"
          >
            <div v-if="isLoading" class="flex items-center justify-center">
              <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              Connexion en cours...
            </div>
            <span v-else>Se connecter</span>
          </button>
        </div>

        <!-- Séparateur -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/20"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-transparent text-white/70">ou</span>
          </div>
        </div>

        <!-- Connexion Google -->
        <button
          @click="handleGoogleLogin"
          class="w-full bg-white/10 hover:bg-white/20 border border-white/20 text-white font-medium py-3 px-4 rounded-xl transition-all duration-300 flex items-center justify-center space-x-3 backdrop-blur-sm hover:scale-105 transform"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          <span>Continuer avec Google</span>
        </button>

        <!-- Inscription -->
        <div class="mt-6 text-center">
          <p class="text-white/70 text-sm">
            Pas encore de compte ?
            <a href="#" class="text-blue-300 hover:text-blue-200 font-medium transition-colors ml-1">
              S'inscrire
            </a>
          </p>
        </div>
      </div>

      <!-- Effet de lueur -->
      <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl blur opacity-30 -z-10"></div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'LoginPage',
  setup() {
    const email = ref('')
    const password = ref('')
    const showPassword = ref(false)
    const isLoading = ref(false)
    const rememberMe = ref(false)

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }

    const handleLogin = async () => {
      if (!email.value || !password.value) {
        alert('Veuillez remplir tous les champs')
        return
      }
      
      isLoading.value = true
      try {
        // Simulation d'une connexion
        await new Promise(resolve => setTimeout(resolve, 1500))
        console.log('Connexion avec:', { 
          email: email.value, 
          password: password.value, 
          rememberMe: rememberMe.value 
        })
        alert('Connexion réussie !')
      } catch (error) {
        console.error('Erreur de connexion:', error)
        alert('Erreur de connexion')
      } finally {
        isLoading.value = false
      }
    }

    const handleGoogleLogin = () => {
      console.log('Connexion avec Google')
      alert('Connexion Google - Intégrez ici votre logique OAuth')
      // Ici vous intégreriez l'API Google OAuth
    }

    return {
      email,
      password,
      showPassword,
      isLoading,
      rememberMe,
      togglePasswordVisibility,
      handleLogin,
      handleGoogleLogin
    }
  }
}
</script>

<style scoped>
/* Animation pour les particules */
@keyframes pulse {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Animation pour le spinner */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>

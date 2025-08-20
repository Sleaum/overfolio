<template>
  <button
    @click="handleSubscription"
    :disabled="loading"
    class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold py-2 px-4 rounded shadow-md transition hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
  >
    <span v-if="loading">Chargement...</span>
    <span v-else>Abonnement - 35€/an</span>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { loadStripe } from '@stripe/stripe-js'

const loading = ref(false)

const STRIPE_PUBLISHABLE_KEY = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const handleSubscription = async () => {
  loading.value = true

  try {
    const response = await fetch(`${API_BASE_URL}/api/create-checkout-session/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'sleaum.gervais@gmail.com', // à remplacer par l'email réel
      }),
    })

    if (!response.ok) throw new Error('Erreur de session')

    const data = await response.json()

    const stripe = await loadStripe(STRIPE_PUBLISHABLE_KEY)
    if (!stripe) throw new Error('Stripe non initialisé')

    await stripe.redirectToCheckout({ sessionId: data.session_id })

  } catch (error) {
    console.error('Erreur abonnement :', error)
    alert('Une erreur est survenue. Veuillez réessayer.')
  } finally {
    loading.value = false
  }
}
</script>


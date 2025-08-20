export const createStripeCheckoutSession = async () => {
  const response = await fetch(`${import.meta.env.VITE_API_BASE}/api/stripe/create-checkout-session/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  })

  if (!response.ok) {
    throw new Error('Erreur lors de la création de la session Stripe')
  }

  return response.json()
}


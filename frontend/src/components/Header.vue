<template>
  <header class="bg-white border-b py-4 mb-10">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
      <h1 class="text-xl font-bold">Overfolio</h1>
      <nav class="space-x-4">
        <a href="http://127.0.0.1/api/googlesheet" class="text-gray-600 hover:text-black">Connexion</a>
        <SubscriptionButton />
      </nav>
    </div>
  </header>
</template>

<script setup>
import SubscriptionButton from './SubscriptionButton.vue'
</script>

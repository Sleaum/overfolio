<template>
  <div>
    <Header />
    <!-- Ici s'affiche la page en fonction de la route -->
    <router-view />
    <Footer />
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
</script>


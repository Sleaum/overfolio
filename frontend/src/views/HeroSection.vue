<template>
  <section class="px-6 py-12 space-y-24">

    <!-- Bloc 1 : Titre + texte centré -->
    <div class="text-center max-w-3xl mx-auto">
      <h2 class="text-4xl font-bold mb-4 text-black">L'allocation avant la sélection</h2>
      <p class="text-lg text-gray-700">
        Impossible de naviguer sans boussole : seule une cartographie exhaustive de ton patrimoine te permet de définir la répartition idéale avant de faire les bons arbitrages entre tes actifs (action, obligation, crypto, immobilier, métal précieux, financement participatif et tous les actifs exotiques).
      </p>
    </div>

    <!-- Bloc 2 : Titre 1 centré + Texte à gauche, image à droite -->
    <div class="max-w-6xl mx-auto">
      <div class="flex flex-col md:flex-row items-center gap-8">
        <div class="md:w-1/2 text-gray-700 text-base space-y-4 text-center md:text-left">
          <h3 class="text-3xl font-semibold text-black text-center">
              Tout part de ton fichier Excel —<br />
              sans prise de tête !
          </h3>
          <p>💡 Tu suis déjà ton patrimoine avec un fichier google sheet ?<br />
             Parfait, nous partons de là.</p>
          <p>🛡️ Tu restes 100 % propriétaire de tes données.</p>
          <ul class="list-disc list-inside space-y-1">
            <li>Pas de collecte de données personnelles.</li>
            <li>Tu gardes le contrôle total, en toute autonomie.</li>
          </ul>
          <p>🌐 Une approche radicalement simple.</p>
          <ul class="list-disc list-inside space-y-1">
            <li>Finis les agrégateurs bancaires flous, intrusifs ou imprécis.</li>
            <li>Pas besoin de changer tes habitudes : tu continues sur google sheet. Nous t’aidons à en tirer une lecture claire et immédiate.</li>
          </ul>
        </div>
        <div class="md:w-1/2">
          <img src="/tableau-excel.png" alt="Visualisation du patrimoine" class="w-full rounded shadow" />
        </div>
      </div>
    </div>

<!-- Bloc 3 : 4 images alternées gauche/droite en grille + texte à droite, fond noir -->
<div class="bg-black py-12">
  <div class="max-w-6xl mx-auto">
    <div class="flex flex-col md:flex-row items-center gap-8">

      <!-- Images en grille 2x2 avec alternance -->
      <div class="md:w-1/2 grid grid-cols-2 grid-rows-2 gap-4">
        <img 
          src="/patrimoine-graph.png" 
          alt="Graphique patrimoine 1" 
          class="w-full rounded shadow"
        />
        <img 
          src="/patrimoine-graph2.png" 
          alt="Graphique patrimoine 2" 
          class="w-full rounded shadow"
        />
        <img 
          src="/patrimoine-graph3.png" 
          alt="Graphique patrimoine 3" 
          class="w-full rounded shadow"
        />
        <img 
          src="/patrimoine-graph4.png" 
          alt="Graphique patrimoine 4" 
          class="w-full rounded shadow"
        />
      </div>

      <!-- Texte -->
      <div class="md:w-1/2 text-white text-base space-y-4 text-center md:text-left">
        <h3 class="text-3xl font-semibold mb-4">
          Visualise tes données en un clin d’œil — automatiquement et magnifiquement.
        </h3>
        <p>
          À partir de ce point d’entrée unique, tu accèdes à une série de visuels clairs qui révèlent ce qu’un simple tableau ne peut pas montrer.
        </p>
        <p>
          Tu comprends d’un coup d’œil ce qui est important, sans jamais changer tes habitudes.
        </p>
        <p>
        Du googlesheet visualise l’ensemble de tes actifs avec des graphiques spécifiques et beaux, afin d’avoir une vision précise de ton portfolio total et ainsi prendre des décisions éclairées de la répartition
        </p>
      </div>

    </div>
  </div>
</div>


  </section>
</template>


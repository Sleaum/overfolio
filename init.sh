#!/bin/bash

echo "🧹 Nettoyage des anciens containers, volumes orphelins..."
docker-compose down --volumes --remove-orphans

echo "🏗️ Build des images..."
docker-compose build --no-cache

echo "🚀 Lancement des services..."
docker-compose up -d

echo "🔍 État des services :"
docker-compose ps

echo "🌐 Application disponible sur : http://localhost"


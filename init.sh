#!/bin/bash
set -e

echo "🧹 Suppression d'éventuels conteneurs résiduels..."
docker rm -f nginx frontend backend db 2>/dev/null || true

echo "🧹 Nettoyage des anciens containers, volumes orphelins..."
docker compose down --volumes --remove-orphans

echo "🏗️ Build des images..."
docker compose build --no-cache

echo "🚀 Lancement des services..."
docker compose up -d

echo "⏳ Attente que la base de données soit prête..."
sleep 15

echo "🔄 Migrations de la base de données..."
docker compose exec backend python manage.py migrate

echo "📁 Collecte des fichiers statiques..."
docker compose exec backend python manage.py collectstatic --noinput

echo "🔍 État des services :"
docker compose ps

echo "📊 Logs des services :"
docker compose logs --tail=20

echo "🌐 Application disponible sur : http://localhost"

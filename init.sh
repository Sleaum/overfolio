#!/bin/bash
set -euo pipefail

RESET=false
NO_CACHE=""

for arg in "$@"; do
  case "$arg" in
    --reset)    RESET=true ;;
    --no-cache) NO_CACHE="--no-cache" ;;
    *) echo "Usage : $0 [--reset] [--no-cache]"; exit 1 ;;
  esac
done

echo "🔎 Vérification de la configuration..."
[ -f .env ] || { echo "❌ Fichier .env introuvable"; exit 1; }

for var in SECRET_KEY POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD; do
  grep -q "^${var}=" .env || { echo "❌ Variable ${var} absente de .env"; exit 1; }
done

if grep -q $'\r' .env; then
  echo "❌ .env contient des fins de ligne Windows (CRLF). Corrige avec : sed -i 's/\r\$//' .env"
  exit 1
fi

docker compose config -q
echo "✅ Configuration valide"

if $RESET; then
  echo "🧹 Arrêt des services et SUPPRESSION des volumes (base de données incluse)..."
  docker compose down --volumes --remove-orphans
else
  echo "🧹 Arrêt des services (les données sont conservées)..."
  docker compose down --remove-orphans
fi

echo "🏗️ Build des images..."
docker compose build $NO_CACHE

echo "🚀 Lancement des services..."
docker compose up -d

echo "⏳ Attente que l'application réponde (db, migrations, backend, nginx)..."
ready=false
for i in $(seq 1 60); do
  if curl -fsS -o /dev/null http://localhost/admin/login/; then
    ready=true
    break
  fi
  sleep 2
done

echo "🔍 État des services :"
docker compose ps -a

if ! $ready; then
  echo "❌ L'application ne répond pas après 2 minutes. Derniers logs :"
  docker compose logs --tail=30 db backend nginx
  exit 1
fi

frontend_exit=$(docker inspect -f '{{.State.ExitCode}}' frontend)
if [ "$frontend_exit" != "0" ]; then
  echo "❌ Le build du frontend a échoué (code ${frontend_exit}) :"
  docker compose logs --tail=30 frontend
  exit 1
fi

echo "🌐 Application disponible sur : http://localhost"
echo "👤 Compte admin : docker compose exec backend python manage.py createsuperuser"

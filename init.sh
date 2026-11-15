#!/bin/bash
set -euo pipefail

RESET=false
SYNC=false
NO_CACHE=""

for arg in "$@"; do
  case "$arg" in
    --reset)    RESET=true ;;
    --sync)     SYNC=true ;;
    --no-cache) NO_CACHE="--no-cache" ;;
    *) echo "Usage : $0 [--reset] [--sync] [--no-cache]"; exit 1 ;;
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

# --- Tables de la base --------------------------------------------------------
# Le backend lance déjà `migrate` à son démarrage : les tables sont créées sans rien faire de plus.
# Ces deux contrôles vérifient simplement que tout est cohérent.
echo "🗄️ Vérification des migrations..."
if ! docker compose exec -T backend python manage.py migrate --check >/dev/null 2>&1; then
  echo "❌ Des migrations ne sont pas appliquées. Logs du backend :"
  docker compose logs --tail=30 backend
  exit 1
fi
echo "✅ Tables de la base à jour"

if ! docker compose exec -T backend python manage.py makemigrations --check --dry-run >/dev/null 2>&1; then
  echo "⚠️  Un modèle a changé sans fichier de migration. Génère-le puis commite-le :"
  echo "    docker compose exec backend python manage.py makemigrations"
fi

# --- Synchronisation Google Sheets -> base (option --sync) ---------------------
sync_failed=false
if $SYNC; then
  echo "📥 Synchronisation des onglets Google Sheets vers la base..."
  if docker compose exec -T backend python manage.py sync_sheets; then
    docker compose exec -T db sh -c \
      'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "select name, row_count, synced_at from googlesheet_sheettable order by name;"'
  else
    sync_failed=true
    echo "⚠️  La synchronisation a échoué (l'application reste utilisable). Détails ci-dessus."
    echo "    Relance-la avec : docker compose exec backend python manage.py sync_sheets"
  fi
elif $RESET; then
  echo "ℹ️  La base vient d'être recréée : les tables sont vides. Lance la synchronisation avec :"
  echo "    docker compose exec backend python manage.py sync_sheets   (ou ./init.sh --sync)"
fi

echo "🌐 Application disponible sur : http://localhost"
echo "👤 Compte admin : docker compose exec backend python manage.py createsuperuser"
$sync_failed && exit 2
exit 0

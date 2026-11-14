# Overfolio

Application Vue.js (frontend) + Django (backend API) + PostgreSQL, orchestrée avec Docker Compose et servie par nginx.

## Structure du projet

```
overfolio/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── overfolio/            # projet Django (settings.py, urls.py, wsgi.py)
├── frontend/
│   └── Dockerfile            # stage "build" (Vite)
├── nginx/
│   └── default.conf
├── .env                      # secrets, NE PAS COMMITER
├── docker-compose.yml
├── init.sh
└── README.md
```

## Prérequis

- Docker et Docker Compose v2 (`docker compose`)
- Un fichier `.env` à la racine (voir ci-dessous)

## Configuration : fichier `.env`

Exemple minimal :

```env
# Django
SECRET_KEY=une_cle_longue_et_aleatoire
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (lu par le conteneur db ET par settings.py)
POSTGRES_DB=overfoliodb
POSTGRES_USER=overfoliouser
POSTGRES_PASSWORD=overfoliopwd

# Google (compte de service)
TYPE=service_account
PROJECT_ID=...
PRIVATE_KEY_ID=...
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=...
CLIENT_ID=...
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=...
UNIVERSE_DOMAIN=googleapis.com
```

Générer une `SECRET_KEY` :

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Règles à respecter :

- Pas d'espaces autour du `=`.
- Fins de ligne Unix (LF). Vérifier avec `grep -c $'\r' .env` : le résultat doit être `0`.
- Les noms doivent être exacts (`POSTGRES_USER`, pas `POSTGRE_USER`).
- Ne jamais commiter `.env` : il doit figurer dans `.gitignore`.

## Lancement

### Première installation ou reconstruction

```bash
chmod +x init.sh
./init.sh
```

Le script :

1. vérifie `.env` (présence, variables obligatoires, absence de CRLF) et la validité du compose ;
2. arrête les services et reconstruit les images ;
3. lance la stack et attend que l'application réponde ;
4. contrôle que le build du frontend s'est terminé avec succès.

Options :

```bash
./init.sh                      # lancement normal (données conservées)
./init.sh --reset              # supprime les volumes : repart d'une base vide
./init.sh --no-cache           # reconstruit les images sans cache
./init.sh --reset --no-cache   # tout reconstruire
```

> `--reset` supprime la base de données. À n'utiliser que si les données sont sans importance.

### Lancement manuel

```bash
docker compose up --build -d
```

### Accès

| URL | Contenu |
|---|---|
| http://localhost | Frontend Vue |
| http://localhost/admin/ | Admin Django |
| http://localhost/api/... | API Django (via nginx) |

Le port 8000 du backend n'est **pas** exposé sur l'hôte : tout passe par nginx.

### Créer un compte administrateur

```bash
docker compose exec backend python manage.py createsuperuser
```

## Architecture

### Les 4 services

| Service | Rôle | Port exposé |
|---|---|---|
| `nginx` | Serveur web, reverse proxy | 80 |
| `frontend` | Build Vue.js/Vite (job one-shot, s'arrête après le build) | aucun |
| `backend` | API Django servie par gunicorn | aucun (8000 interne) |
| `db` | PostgreSQL 15 | aucun (5432 interne) |

### Ordre de démarrage

```
db (healthy) ──► backend (migrate + collectstatic + gunicorn) ──┐
frontend (build, exit 0) ───────────────────────────────────────┴──► nginx
```

- `backend` attend que `db` soit **healthy** (`pg_isready`).
- `nginx` attend que le build `frontend` soit **terminé avec succès** (`service_completed_successfully`) et que `backend` soit démarré.
- Le conteneur `frontend` en statut `Exited (0)` est le comportement normal.

### Communication interne (réseau Docker)

| Émetteur | Accède à | Pourquoi | Adresse |
|---|---|---|---|
| nginx | frontend (build) | Sert les fichiers `dist` | volume `frontend-dist` monté sur `/usr/share/nginx/html` |
| nginx | backend | Proxy `/api/` et `/admin/` | `http://backend:8000` |
| nginx | backend (statiques) | Sert `/static/` | volume `static_data` monté sur `/staticfiles` |
| backend | db | Accès PostgreSQL | `db:5432` |

### Communication externe (navigateur)

| Qui | Fait quoi | Comment |
|---|---|---|
| Navigateur | Ouvre l'interface Vue | `http://localhost` (port 80) |
| Frontend (dans le navigateur) | Appelle l'API | chemins relatifs `/api/...`, redirigés par nginx vers le backend |

> Le code Vue doit utiliser des URLs relatives (`/api/...`) et non `http://localhost:8000/api/...`.

### Vue d'ensemble

```
                    🌍 Navigateur
                          │
                   http://localhost
                          │
                      [nginx:80]
              ┌───────────┼─────────────┐
              │           │             │
        fichiers Vue   /api, /admin   /static
        (volume dist)     │         (volume static_data)
                          ▼
                   [backend:8000]
                    gunicorn + Django
                          │
                          ▼
                     [db:5432]
                    PostgreSQL
```

## Commandes utiles

```bash
docker compose ps -a                    # état des services
docker compose logs -f backend          # logs du backend en direct
docker compose logs --tail 30 nginx     # derniers logs nginx
docker compose config                   # valide et affiche le compose
docker compose down                     # arrête (données conservées)
docker compose down -v                  # arrête ET supprime la base

# Tester la config nginx sans lancer la stack
docker run --rm \
  -v "$PWD/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro" \
  --add-host backend:127.0.0.1 \
  nginx:alpine nginx -t

# Accès à la base
docker compose exec db psql -U overfoliouser -d overfoliodb
```

## Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `yaml: could not find expected ':'` | Clé mal indentée, tabulation ou espace insécable | `cat -A docker-compose.yml`, puis `docker compose config` |
| `SECRET_KEY not found in environment variables` | Variable absente ou mal nommée dans `.env` | Corriger `.env`, relancer |
| `db` reste `unhealthy`, `backend` en `Created` | Healthcheck en échec | `docker inspect --format '{{range .State.Health.Log}}{{.Output}}{{end}}' db` |
| `role "..." does not exist` | Volume initialisé avec d'anciens identifiants | `docker compose down -v` puis relancer |
| `host not found in upstream "backend"` | Backend non démarré | `docker compose logs backend` |
| `502 Bad Gateway` | nginx ne joint pas le backend | Vérifier que `backend` est `Up` |
| `404` sur `/api/` | Pas de route à la racine de l'API | Tester un vrai endpoint |
| `unknown directive` (nginx) | Faute de frappe dans `default.conf` | Lancer `nginx -t` (commande ci-dessus) |
| `git push` : mot de passe refusé | GitHub n'accepte plus les mots de passe | Utiliser une clé SSH ou un token |

> Les identifiants PostgreSQL ne sont lus qu'à la **première initialisation** du volume. Si tu les modifies dans `.env`, il faut recréer le volume (`docker compose down -v`).

## Sécurité

- `.env` ne doit jamais être commité.
- Si une clé privée a été exposée (capture d'écran, commit), la révoquer dans Google Cloud (IAM → Comptes de service → Clés) et en générer une nouvelle.
- Passer à `DEBUG=False` et restreindre `ALLOWED_HOSTS` en production.

## Notes pour la production

- Retirer le montage `./backend:/app` du service `backend`.
- Utiliser un Dockerfile frontend multi-stage (build Node, puis copie du `dist` dans une image nginx).
- Mettre en place HTTPS (certificat, `SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS`).
- Sauvegarder régulièrement le volume `postgres_data`.

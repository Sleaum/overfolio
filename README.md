## create
overfolio/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
├── frontend/
│   ├── Dockerfile
├── nginx/
│   └── default.conf
├── .env
├── docker-compose.yml
└── README.md

docker-compose run --rm backend django-admin startproject myproject .

## launch
docker-compose up --build
localhost:8000
localhost/api/googlesheet

## new launch
./init.sh
localhost

## explication new launch
⚙️ Les 4 services
Service	Rôle	Port exposé
nginx	Serveur web qui reçoit les requêtes	80
frontend	Application Vue.js compilée (statique)	aucun (build seulement)
backend	Application Django ou autre API	8000
db	Base de données PostgreSQL	aucun

📡 Comment ils communiquent
🔁 Communication interne (Docker network) :
Émetteur	Accède à	Pourquoi ?	Adresse utilisée
nginx	frontend (build statique)	Sert les fichiers dist	via volume monté (/usr/share/nginx/html)
nginx	backend	Proxy les appels /api	http://backend:8000
backend	db	Accès base PostgreSQL	db:5432 (nom du service)

🌍 Communication externe (depuis ton navigateur) :
Qui ?	Fait quoi ?	Comment ?
Toi (navigateur)	Accède à l’UI Vue	http://localhost (port 80)
Frontend (dans navigateur)	Fait des appels API	/api/... → redirigé par nginx → backend

🧭 Vue d’ensemble
Voici un schéma visuel :

                        🌍 Navigateur (Toi)
                                │
                          http://localhost
                                │
                            [NGINX:80]
                           /        \
              sert fichiers      proxy /api
              frontend dist       vers backend
                 (volume)            |
                                 [Backend:8000]
                                      |
                                   [DB:5432]
                                (PostgreSQL)
🧩 Résumé
Tu ouvres ton navigateur → http://localhost
NGINX sert les fichiers Vue (dist/)
Quand Vue fait une requête /api/..., NGINX la redirige vers backend
Backend parle à la base de données (db)



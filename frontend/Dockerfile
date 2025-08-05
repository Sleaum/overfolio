# Étape 1 : Construction de l'app
FROM node:20-alpine AS build

WORKDIR /app

# Copie tous les fichiers
COPY . .

# Installe les dépendances + build Vite
RUN npm install && npm run build

# Étape finale : NGINX
FROM nginx:alpine

# Copie le build vers le dossier public d’NGINX
COPY --from=build /app/dist /usr/share/nginx/html

# Copier ta conf nginx personnalisée si besoin
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


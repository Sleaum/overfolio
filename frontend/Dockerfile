# Étape 1 : build de l'app Vue
FROM node:20-alpine AS build

WORKDIR /app

# Copie des dépendances
COPY package*.json ./
RUN npm install

# Copie du reste des fichiers et build
COPY . .
RUN npm run build


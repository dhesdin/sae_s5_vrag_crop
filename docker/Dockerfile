FROM node:lts-alpine

# installe un simple serveur http pour servir un contenu statique
RUN npm install -g http-server

WORKDIR /app

# copie package.json et package-lock.json depuis le dossier frontend
COPY frontend/package*.json ./

RUN npm install

# copie le reste du projet frontend
COPY frontend/ .

# construit l'app pour la production
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]
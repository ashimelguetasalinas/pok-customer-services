# Dockerfile.dev
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install -D vite-tsconfig-paths
RUN npm install @nuxtjs/color-mode
RUN npm install jwt-decode
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

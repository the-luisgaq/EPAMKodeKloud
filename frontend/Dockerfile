# Etapa 1: Build de la app con Node
FROM node:20 AS builder

WORKDIR /app

# Ensure dev dependencies like Vite are installed
ENV NODE_ENV=development

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: Servir con NGINX
FROM nginx:stable-alpine

# Copia los archivos de build al directorio de NGINX
COPY --from=builder /app/dist /usr/share/nginx/html

# Opcional: copia tu archivo nginx.conf si quieres configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
